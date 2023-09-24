def inject_parameter_info_doc_strings(*sub):
    def decode(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj

    return decode
