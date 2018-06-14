Intel ME Manufacturing Mode Detection Tools
=====
This repository contains Python 2.7 scripts for checking the state of the Intel ME Manufacturing Mode.

## Manufacturing Mode

Intel ME has a Manufacturing Mode designed to be used exclusively by motherboard manufacturers. This mode provides some additional opportunities that an attacker can take advantage of. When Manufacturing Mode is enabled, Intel ME allows execution of the command which makes the ME region writable via the SPI controller built into the motherboard. The ability to run code and send commands to Intel ME on the attacked system allows the attacker to rewrite the Intel ME firmware onto another version. So the attacker is able to deploy the firmware which is vulnerable to [INTEL-SA-00086][7] and execute arbitrary code on Intel ME even if the system is patched.

## Usage

	mmdetect.py [-h] [--path PATH]

	Manufacturing mode detection tool.

	optional arguments:
		-h, --help   show this help message and exit
		--path PATH  path to lspci binary

## Limitations

  1. Tools work only if HECI device isn't hidden.
  2. 'pciutils' library ([WIN][6], [LIN][5]) is required.
  3. 'requests' library is needed for installing 'pciutils' on Windows.

	pip install requests


## Related URLs:

[How to Hack a Turned-Off Computer or Running Unsigned Code in Intel Management Engine][1]

[CVE-2018-4251 (MacOS High Sierra 10.13.5, Security Update)][8]

## Author

Maxim Goryachy ([@h0t_max][3])

## Research Team

Mark Ermolov ([@\_markel___][2])

Maxim Goryachy ([@h0t_max][3])

Dmitry Sklyarov ([@_Dmit][4])

## License
This software is provided under a custom License. See the accompanying LICENSE file for more information.

[1]: https://www.blackhat.com/eu-17/briefings.html#how-to-hack-a-turned-off-computer-or-running-unsigned-code-in-intel-management-engine
[2]: https://twitter.com/_markel___
[3]: https://twitter.com/h0t_max
[4]: https://twitter.com/_Dmit
[5]: https://github.com/pciutils/pciutils
[6]: https://eternallybored.org/misc/pciutils/
[7]: https://www.intel.com/content/www/us/en/security-center/advisory/intel-sa-00086.html
[8]: https://support.apple.com/en-ca/HT208849
