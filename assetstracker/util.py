import re
from operator import and_, or_
from django.db.models import Q

def get_filters(params):
    """"
    It parses querset that is formatted as:
    /api/offices?filter[country][]=1&filter[country][]=2&filter[name][]=KBL&filter[name][]=KND&filter[long_name]=Kabul

    To test is in Ember using Chrome Console:
    console out an instance of the Ember.js store object in your Ember app
    in the cosnsole window, right click on the store class and set it as Global
    store = temp1
    offices = store.query('office', {filter: {country: ["1", "2",], name: ['KBL', 'KND',],long_name: 'Kabul' }});
    offices.forEach(function(o){console.log(o.get('name'));});
    """
    kwargs = {}
    args = []

    for key, val in params.iteritems():
        # retrieves the field name from the filter query string.
        field = re.search(r"\[([A-Za-z0-9_]+)\]", key).group(1)

        # if the val is a list with > 1 values in it, then use Q objects
        if len(val) > 1:
            args.append(reduce(or_, [Q(**{field:v}) for v in val] ) )
        else:
            kwargs[field] = str(val[0])
    return (args, kwargs)