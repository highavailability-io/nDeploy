#!/usr/bin/python

import cgi
import cgitb
import os
import psutil
import platform
import yaml
import sys
from commoninclude import print_nontoast_error, bcrumb, print_header, print_footer, display_term, cardheader, cardfooter


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
default_domain_data_file = installation_path+'/conf/domain_data_default.yaml'
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"

cgitb.enable()

form = cgi.FieldStorage()

print_header('Upstream Settings')
bcrumb('Upstream Settings','fas fa-box-open')

if form.getvalue('cpanelpkg') and form.getvalue('backend'):
    if form.getvalue('cpanelpkg') == 'default':
        pkgdomaindata = installation_path+'/conf/domain_data_default_local.yaml'
    else:
        pkgdomaindata = installation_path+'/conf/domain_data_default_local_'+form.getvalue('cpanelpkg')+'.yaml'
    mybackend = form.getvalue('backend')

    # Get data about the backends available
    if os.path.isfile(backend_config_file):
        with open(backend_config_file, 'r') as backend_data_yaml:
            backend_data_yaml_parsed = yaml.safe_load(backend_data_yaml)
    if os.path.isfile(pkgdomaindata):

        # Get all config settings from the domains domain-data config file
        with open(pkgdomaindata, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)

        # App settings
        backend_category = yaml_parsed_profileyaml.get('backend_category')
        backend_version = yaml_parsed_profileyaml.get('backend_version')
        backend_path = yaml_parsed_profileyaml.get('backend_path')
        apptemplate_code = yaml_parsed_profileyaml.get('apptemplate_code')

        # Get the human friendly name of the app template
        if os.path.isfile(app_template_file):
            with open(app_template_file, 'r') as apptemplate_data_yaml:
                apptemplate_data_yaml_parsed = yaml.safe_load(apptemplate_data_yaml)
            apptemplate_dict = apptemplate_data_yaml_parsed.get(backend_category)
            if apptemplate_code in apptemplate_dict.keys():
                apptemplate_description = apptemplate_dict.get(apptemplate_code)
        else:
            print_nontoast_error('Error!', 'Application Template Data File Error!')
            sys.exit(0)

        # Ok we are done with getting the settings,now lets present it to the user

        # Cpanel Package App Status
        print('            <!-- WHM Starter Row -->')
        print('            <div class="row justify-content-lg-center">')
        print('                <!-- First Column Start -->')
        print('                <div class="col-lg-8">')
        print('')

        cardheader(form.getvalue('cpanelpkg')+' cPanel Package','fas fa-box-open')
        print('                    <div class="card-body p-0"> <!-- Card Body Start -->')
        print('                        <div class="row no-gutters row-2-col"> <!-- Row Start -->')

        nginx_status = False
        for myprocess in psutil.process_iter():
            # Workaround for Python 2.6
            if platform.python_version().startswith('2.6'):
                mycmdline = myprocess.cmdline
            else:
                mycmdline = myprocess.cmdline()
            if '/usr/sbin/nginx' in mycmdline or 'nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf' in mycmdline:
                nginx_status = True
                break

        if nginx_status:
            print('                        <div class="col-md-6 alert"><i class="fas fa-play"></i>&nbsp;Nginx</div>')
            print('                        <div class="col-md-6 alert text-success"><i class="fas fa-check"></i>&nbsp;Active</div>')
        else:
            print('                        <div class="col-md-6 alert"><i class="fas fa-play"></i>&nbsp;Nginx</div>')
            print('                        <div class="col-md-6 alert text-danger"><i class="fas fa-times"></i>&nbsp;Inactive</div>')

        # Backend
        print('                            <div class="col-md-6 alert"><i class="fas fa-server"></i>&nbsp;Current&nbsp;Upstream</div>')
        print('                            <div class="col-md-6 alert text-success">'+backend_version+'</div>')

        # Description
        print('                            <div class="col-md-6 alert"><i class="fas fa-cog"></i>&nbsp;Current Template</div>')
        print('                            <div class="col-md-6 alert text-success">'+apptemplate_description+'</div>')

        # .htaccess
        if backend_category == 'PROXY' and backend_version == 'httpd':

            print('                        <div class="col-md-6 alert"><i class="fas fa-file-code"></i>&nbsp;Current&nbsp;.htaccess&nbsp;Status</div>')
            print('                        <div class="col-md-6 alert text-success"><i class="fas fa-check"></i>&nbsp;</div>')

        else:

            print('                        <div class="col-md-6 alert"><i class="fas fa-file-code"></i>&nbsp;Current&nbsp;.htaccess&nbsp;Status</div>')
            print('                        <div class="col-md-6 alert text-danger"><i class="fas fa-times"></i>&nbsp;Ignored</div>')

        # New Upstream
        print('                            <div class="col-md-6 alert"><i class="fas fa-server"></i>&nbsp;New&nbsp;Upstream&nbsp;Type</div>')
        print('                            <div class="col-md-6 alert text-warning text-center">'+mybackend+'</div>')

        print('                        </div> <!-- Row End -->')
        print('                    </div> <!-- Card Body End -->')

        print('                    <div class="card-body"> <!-- Card Body Start -->')

        print('                        <div class="alert alert-info text-center mb-4">')
        print('                            You selected <span class="p-2 badge badge-warning">'+mybackend+'</span> as the new upstream type <br>for the '+form.getvalue('cpanelpkg')+' package. Select the desired <br>version and template for this cPanel Package.')
        print('                        </div>')

        backends_dict = backend_data_yaml_parsed.get(mybackend)
        new_apptemplate_dict = apptemplate_data_yaml_parsed.get(mybackend)
        print('                        <form class="form" method="post" id="save_pkg_app_settings" onsubmit="return false;">')

        if mybackend == backend_category:
            print('                        <div class="input-group">')
            print('                            <div class="input-group-prepend input-group-prepend-min">')
            print('                                <label class="input-group-text">Upstream</label>')
            print('                            </div>')
            print('                            <select name="backendversion" class="custom-select">')
            for mybackend_version in backends_dict.keys():
                if mybackend_version == backend_version:
                    print('                        <option selected value="'+mybackend_version+'">'+mybackend_version+'</option>')
                else:
                    print('                        <option value="'+mybackend_version+'">'+mybackend_version+'</option>')
            print('                            </select>')
            print('                        </div>')

            print('                        <div class="input-group">')
            print('                            <div class="input-group-prepend input-group-prepend-min">')
            print('                                <label class="input-group-text">Config Template</label>')
            print('                            </div>')
            print('                            <select name="apptemplate" class="custom-select">')
            for myapptemplate in sorted(new_apptemplate_dict.keys()):
                if myapptemplate == apptemplate_code:
                    print('                        <option selected value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>')
                else:
                    print('                        <option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>')
            print('                            </select>')
            print('                        </div>')
        else:
            print('                        <div class="input-group">')
            print('                            <div class="input-group-prepend input-group-prepend-min">')
            print('                                <label class="input-group-text">Upstream</label>')
            print('                            </div>')
            print('                            <select name="backendversion" class="custom-select">')
            for mybackend_version in backends_dict.keys():
                print('                            <option value="'+mybackend_version+'">'+mybackend_version+'</option>')
            print('                            </select>')
            print('                        </div>')
            print('                        <div class="input-group">')
            print('                            <div class="input-group-prepend input-group-prepend-min">')
            print('                                <label class="input-group-text">Config template</label>')
            print('                            </div>')
            print('                            <select name="apptemplate" class="custom-select">')
            for myapptemplate in sorted(new_apptemplate_dict.keys()):
                print('                            <option value="'+myapptemplate+'">'+new_apptemplate_dict.get(myapptemplate)+'</option>')
            print('                            </select>')
            print('                        </div>')

        # Pass on the domain name to the next stage
        print('                            <input hidden name="cpanelpkg" value="'+form.getvalue('cpanelpkg')+'">')
        print('                            <input hidden name="backend" value="'+mybackend+'">')
        print('                            <button id="save-pkg-app-settings-btn" class="btn btn-outline-primary btn-block mt-4" type="submit">Update Package</button>')
        print('                        </form> <!-- save_pkg_app_settings end -->')
        print('                    </div> <!-- Card Body End -->')
        cardfooter('')

    else:
        print_nontoast_error('Forbidden!', 'Missing cPanel Package Data File!')
        sys.exit(0)

else:
    print_nontoast_error('Forbidden!', 'Missing cPanel Package or Backend Data!')
    sys.exit(0)

#Column End
print('                        </div> <!-- Column End -->')
print('')
print('                    </div> <!-- WHM End Row -->')

print_footer()
