#include <windows.h>
#include <cstdio>
#include <intrin.h>

bool IsVM()
{
    int cpuInfo[4] = {};

    //
    // Upon execution, code should check bit 31 of register ECX
    // (the “hypervisor present bit”). If this bit is set, a hypervisor is present.
    // In a non-virtualized environment, the bit will be clear.
    //
    __cpuid(cpuInfo, 1);
    
    if (!(cpuInfo[2] & (1 << 31)))
        return false;
    
    //
    // A hypervisor is running on the machine. Query the vendor id.
    //
    const auto queryVendorIdMagic = 0x40000000;
    __cpuid(cpuInfo, queryVendorIdMagic);

    const int vendorIdLength = 13;
    using VendorIdStr = char[vendorIdLength];

    VendorIdStr hyperVendorId = {};
    
    memcpy(hyperVendorId + 0, &cpuInfo[1], 4);
    memcpy(hyperVendorId + 4, &cpuInfo[2], 4);
    memcpy(hyperVendorId + 8, &cpuInfo[3], 4);
    hyperVendorId[12] = '\0';

    static const VendorIdStr vendors[]{
    "KVMKVMKVM\0\0\0", // KVM 
    "Microsoft Hv",    // Microsoft Hyper-V or Windows Virtual PC */
    "VMwareVMware",    // VMware 
    "XenVMMXenVMM",    // Xen 
    "prl hyperv  ",    // Parallels
    "VBoxVBoxVBox"     // VirtualBox 
    };

    for (const auto& vendor : vendors)
    {
        if (!memcmp(vendor, hyperVendorId, vendorIdLength))
            return true;
    }

    return false;
}

bool IsVMRunning()
{
#if _WIN64
    UINT64 time1 = __rdtsc();
    UINT64 time2 = __rdtsc();
    return ((time2 - time1) > 500);
#else
    unsigned int time1 = 0;
    unsigned int time2 = 0;
    __asm
    {
        RDTSC
        MOV time1, EAX
        RDTSC
        MOV time2, EAX
    }
    return ((time2 - time1) > 500);
#endif
}

int main()
{
    if (!IsVM() and !IsVMRunning())
    {
        MessageBox(NULL, L"Hi there!", L"Greetings.exe", MB_OK);
    }
    else
    {
        MessageBox(NULL, L"Oh, no, It's VM!", L"Sad.exe", MB_OK);
    }
    system("pause");
    return 0;
}
