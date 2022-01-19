import wmi

c = wmi.WMI()
# for os in c.Win32_OperatingSystem():
#     print(os)

# Monitora os programas que estão sendo abertos
# process_watcher = c.Win32_Process.watch_for("creation")
# while True:
#   new_process = process_watcher()
#   print(new_process.Caption)

# Não sei o que faz
# for service in c.Win32_Service(Name="seclogon"):
#     result, = service.StopService()
#     if result == 0:
#         print("Service", service.Name, "stopped")
#     else:
#         print("Some problem")
#     break
# else:
#     print("Service not found")

# Discos Fisicos
# for disk in c.Win32_LogicalDisk(["Caption", "Description"], DriveType=3):
#     print(disk)

# Discos Fisicos e de rede
# wql = "SELECT Caption, Description FROM Win32_LogicalDisk WHERE DriveType <> 3"
# for disk in c.query(wql):
#     print(disk)
# c = wmi.WMI(privileges=["Security"])
# watcher = c.Win32_NTLogEvent.watch_for("creation", 2, Type="error")
# while 1:
#     error = watcher()
#     print("Error in %s log: %s" % (error.Logfile, error.Message))

# # Placas de Redes e IPS
# nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)
# print(nic_configs)
# for nic in nic_configs:
#     print(nic)
for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
    print(interface.Description, interface.MACAddress)
    for ip_address in interface.IPAddress:
        print(ip_address)
    print()


# Impressoras
# for printer in c.win32_printer():
#     print(printer)

# Shared Folders
for share in c.Win32_Share():
    print(share.Name, share.Path)

# What’s running on startup and from where?
for s in c.Win32_StartupCommand():
    print("[%s] %s <%s>" % (s.Location, s.Caption, s.Command))

# # Watch for errors in the event log
# c = wmi.WMI(privileges=["Security"])
# watcher = c.watch_for(
#     notification_type="Creation",
#     wmi_class="Win32_NTLogEvent",
#     Type="error"
# )
# while 1:
#     error = watcher()
#     print("Error in %s log: %s" %  (error.Logfile, error.Message))


# Show disk partitions
for physical_disk in c.Win32_DiskDrive():
    for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
        for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
            print(physical_disk.Caption, partition.Caption, logical_disk.Caption)


# Find Drive Types
DRIVE_TYPES = {
    0: "Unknown",
    1: "No Root Directory",
    2: "Removable Disk",
    3: "Local Disk",
    4: "Network Drive",
    5: "Compact Disc",
    6: "RAM Disk"
}
c = wmi.WMI()
for drive in c.Win32_LogicalDisk():
    print(drive.Caption, DRIVE_TYPES[drive.DriveType])
