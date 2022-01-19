import wmi

c = wmi.WMI ()

# Mostra sistema operacional
print(c.Win32_OperatingSystem()[0].Caption)
# print(c.Win32_OperatingSystem()[0])

# print(c.Win32_PowerManagementEvent.derivation())

# print(c.Win32_ComputerSystem.methods.keys())

# os = c.Win32_OperatingSystem
# for method_name in os.methods:
#     method = getattr(os, method_name)
#     print(method)


# c = wmi.WMI(find_classes=False)
# # for i in c.Win32_Process(["Caption", "ProcessID"]):
# for i in c.Win32_Process():
#     print(i)

# Processos
# for process in c.Win32_Process ():
#   print(process.ProcessId, process.Name)

# Servicos que iniciam com o Windows
# services = c.Win32_Service (StartMode="Auto", State="Stopped")
# services = c.Win32_Service()
# for s in services:
#     print(s)

# Programas que iniciam com o Windows
for s in c.Win32_StartupCommand ():
  print("[%s] %s <%s>" % (s.Location, s.Caption, s.Command))    

# Mostra os discos e suas caracteristicas
# for discos in c.Win32_LogicalDisk():
#     print(discos)

# Mostra dados do Computador
# for computador in c.Win32_ComputerSystem():
#     print(computador)

# Mostra placas de rede
# wql = "SELECT IPAddress FROM Win32_NetworkAdapterConfiguration WHERE IPEnabled = 'True'"
# wql = "SELECT * FROM Win32_NetworkAdapterConfiguration WHERE IPEnabled = 'True'"
# wql = "SELECT * FROM Win32_NetworkAdapterConfiguration"

# for placa in c.query(wql):
#     print(placa)


# for s in c.Win32_Service(StartMode="Auto", State="Stopped"):
#     if input("Restart %s? " % s.Caption).upper() == "Y":
#         s.StartService()