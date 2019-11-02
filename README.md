# bomb3r 💣

Made with ❤ in IN.

## For Windows 10/8.x/7

> Use windows [releases](https://github.com/iMro0t/bomb3r/releases)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/installing/) to install bomb3r.

```bash
git clone https://github.com/iMro0t/bomb3r.git
cd bomb3r
pip3 install -r requirements.txt
```

## Usage

```bash
python3 bomb.py <TARGET>
```

where TARGET is target mobile number.

## Options

```
usage: bomb.py [-h] [--sms SMS] [--threads THREADS] TARGET

positional arguments:
  TARGET                    Target mobile number without country code (default:+91)

optional arguments:
  -h, --help                show this help message and exit
  --sms SMS, -S SMS         Number of sms to target (default: 10)
  --threads THREADS, -T THREADS
                            Number of threads (default: 10)
```

## License

This project is licensed under the [GNU General Public License v3.0](https://github.com/iMro0t/bomb3r/blob/master/LICENSE)
