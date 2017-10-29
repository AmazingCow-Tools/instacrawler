################################################################################
## Imports                                                                    ##
################################################################################
## Python
import os.path;

################################################################################
## Public Vars                                                                ##
################################################################################
base_path = ".";


################################################################################
## Public Functions                                                           ##
################################################################################
def fs_create_user_dir(username):
    os.system("mkdir -p {0}".format(username));

def fs_exists(path):
    return os.path.exists(path);

def fs_build_save_path(name, src):
    if(src is None):
        return None;

    path = os.path.basename(src);
    path = os.path.join(name, path);

    return path;


def fs_dump_errors(username, urls, download_urls):
    f = open(build_save_path(username, "errors.txt"), "a");
    for url in urls:
        f.write("Url: {0}\n".format(url));

    for url in download_urls:
        f.write("Media: {0}\n".format(url));

    f.close();
