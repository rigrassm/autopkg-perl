#!/usr/bin/env python3

import json
import requests
import pprint


def get_module_info(perl_module, base='https://fastapi.metacpan.org'):
    search_url = "{base}/release/{mod_name}".format(base=base, mod_name=perl_module)
    result = requests.get(search_url)
    return result.json()


def post_search(base, q):
    # Leaving this function here but I don't think it will be used for API calls as the data returned is in a less than
    # optimal format for our use cases.

    search_url = "{base}/{ep}".format(base=base, ep="v1/release/_search")
    result = requests.get(search_url, data=json.dumps(q))
    return result.json()


def strip_dbl_colons(text):
    if type(text) is dict:
        is_dict = True
        mod_names_string = json.dumps(text)
    else:
        is_dict = False
        mod_names_string = text
    stripped = str(mod_names_string).replace('::', '-')

    return json.loads(stripped) if is_dict else stripped


def get_requires(mod_data, recommends=False, suggests=False):
    # This function is a little more in depth then the name would indicate, it takes the modules configure and runtime
    # dependencies and returns them in the Solus Package naming scheme. This will make generating package.yml files a
    # fairly smooth process.

    pre_reqs = mod_data["prereqs"]
    mod_name = mod_data["name"]

    req_types_list = ["configure", "runtime"]
    req_level = ["requires"]

    if recommends:
        req_level.append("recommends")
    if suggests:
        req_level.append("suggests")

    requires = {mod_name: {"reqs": {"configure": {}, "runtime": {}}}}

    for item in req_types_list:
        if item in pre_reqs:
            for level in req_level:
                if level in pre_reqs[item]:
                    stripped = strip_dbl_colons(pre_reqs[item][level])
                    requires[mod_name]["reqs"][item][level] = {gen_eopkg_name(k): v for (k, v) in stripped.items()}

    return requires


def gen_perl_mod_name(mod_data):
    # May work. May not... wouldn't rely on this one too heavily
    mod_name = mod_data["distribution"]
    return "{}".format(str(mod_name).replace('-', '::'))


def gen_eopkg_name(module_name):
    # Takes a Perl Module in the Perl::Module::Format and returns a compliant Solus Perl module package name

    prefix = 'perl-'
    return "{prefix}{mod_name}".format(prefix=prefix,
                                       mod_name=strip_dbl_colons(module_name)).lower()


def _wrap_print(header, body):
    pp = pprint.PrettyPrinter(width=30)
    print("=" * 60)
    print(header)
    print("=" * 60)
    pp.pprint(body)
    print("")


def main(modules):
    base_url = 'https://fastapi.metacpan.org'

    for mod in modules:
        data = get_module_info(mod, base_url)
        requirements = get_requires(mod_data=data["metadata"], recommends=True)

        _wrap_print(header="{} - Version {}".format(gen_perl_mod_name(data), data['version']),
                    body=requirements[mod]["reqs"]
                    )


if __name__ == '__main__':
    test_modules = ["HTTP-Tiny", "Moose", "Try-Tiny"]
    main(test_modules)
