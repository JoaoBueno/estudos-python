import optparse

parser = optparse.OptionParser()

parser.add_option('-i', '--interface', dest='interface', help='Interface to change MAC address')
parser.add_option('-m', '--mac', dest='new_mac', help='New MAC address')

(options, arguments) = parser.parse_args()

interface = options.interface
new_mac = options.new_mac
print(interface)
print(new_mac)
