# autopkg-perl
Utility for automatically generating eopkg's for perl modules using the [MetaCPAN](https://fastapi.metacpan.org/) API for sourcing the necessary packaging data

# Usage
In it's current form it's just grabbing some Perl module data that will be used in the future for generating eopkgs
automatically.

```[]
python3 autopkg-perl
```

You can edit the list of Perl modules in the `main()` function to test against different Perl modules. The names must match
the name of the module listed on MetaCPAN

## Example Output
**/usr/bin/python3.5 /home/rigrassm/Development/github/autopkg-perl/autopkg-perl.py**

```
============================================================
HTTP-Tiny - Version 0.070
============================================================

{'configure': {'requires': {'perl-extutils-makemaker': '6.17',
                            'perl-perl': '5.006'}},
 'runtime': {'recommends': {'perl-http-cookiejar': '0.001',
                            'perl-io-socket-ip': '0.32',
                            'perl-io-socket-ssl': '1.42',
                            'perl-mozilla-ca': '20160104',
                            'perl-net-ssleay': '1.49'},
             'requires': {'perl-bytes': '0',
                          'perl-carp': '0',
                          'perl-fcntl': '0',
                          'perl-io-socket': '0',
                          'perl-mime-base64': '0',
                          'perl-perl': '5.006',
                          'perl-socket': '0',
                          'perl-strict': '0',
                          'perl-time-local': '0',
                          'perl-warnings': '0'}}}

```

The requirements are converted to match the Solus naming scheme for perl
modules provided by it's repositories. Right now, this conversion is not
reversible due to the names being converted to lower case. Future work
will be done to provide a sane way for preserving the original name.

## Example
###### Perl Syntax
- HTTP::Tiny

###### Solus Package Name
* perl-http-tiny

## Links
- [Solus-Project - About](https://solus-project.com/solus/about)
- [Solus-Project - Packaging Guidelines](https://solus-project.com/articles/packaging/https://solus-project.com/solus/about)
- [MetaCPAN - API v1 Documentation](https://fastapi.metacpan.org/)