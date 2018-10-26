from bs4 import BeautifulSoup


def extract_from (file_path):
    raw_html = open(file_path).read()
    html = BeautifulSoup(raw_html, 'html.parser')
    return_dict = dict()
    for div in html.find_all('div', "Aspf-ListCtrl-Row"):

        # find all div with class name "Aspf-ListCtrl-Row"
        if 'oListDevices' in div['id']:
            return_dict[div['id']] = dict()


            div_attrs = div.attrs
            # < div id = "Row:0:oListDevices" class ="Aspf-ListCtrl-Row"    value="13063:device"  sNetworkAddress="10.136.38.143" nDeviceID="13063"  nParentGroupID="2545" >
            if 'ndeviceid' in div_attrs:
                return_dict[div['id']].update({'nDeviceID': div_attrs['ndeviceid']})
            else:
                return_dict[div['id']].update({'nDeviceID': 'unknown'})

            if 'nParentGroupID' in div_attrs:    
                return_dict[div['id']].update({'nParentGroupID': div_attrs['nParentGroupID'.lower()]})
            else:
                return_dict[div['id']].update({'nParentGroupID': 'unknown'})

            return_dict[div['id']].update({'row': int(row_number(div['id']))})
            return_dict[div['id']]['col'] = dict()
            for deeper_div in div.find_all('div'):
                id_name = deeper_div['id']
                return_dict[div['id']]['col'][int(column_number(id_name))] = deeper_div.text
                # return_dict[div['id']]['col'].update({'colnumber': column_number(id_name)})
    return return_dict


def column_number(id_name):
    # example of id name :'Row:42:Col:2:oListDevices'
    name_split = id_name.split(':')
    return name_split[3]

def row_number(id_name):
    # example of id name :'Row:42:oListDevices'
    name_split = id_name.split(':')
    return name_split[1]

if "__main__" == __name__:
    print(extract_from('html_imports\\raw_html.txt'))
