from fingerprint.models import Fingerprint
from public.models import PublicFingerprintShare

def hasFingerprintPermissions(request, fingerprint_id):

    if request.user.is_authenticated():
        return True
    else:
        public_key = request.POST.get('publickey')
        print public_key
        try:
            public_link = PublicFingerprintShare.objects.get(hash=public_key)

            if public_link.fingerprint.fingerprint_hash == fingerprint_id:
                return True

        except PublicFingerprintShare.DoesNotExist:
            pass
        

    return False