import os
def upload_to_path(instance, filename):
    '''create unique-path & filename for upload'''
    #get the extension name
    ext=filename.split('.')[-1]
    filename = "%s.%s" % ('img', ext)
    s="_"
    return os.path.join("images",s.join(['user',str(instance.user.pk)]),s.join(['deal',str(instance.deal.pk),str(instance.deal.type)]),filename)