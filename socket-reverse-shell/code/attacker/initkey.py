import rsa
(pubkey, privkey) = rsa.newkeys(512)

pub = pubkey.save_pkcs1()
pubfile = open('attpublic.pem','wb')
pubfile.write(pub)
pubfile.close()

pri = privkey.save_pkcs1()
prifile = open('attprivate.pem','wb')
prifile.write(pri)
prifile.close()

(pubkey, privkey) = rsa.newkeys(1024)

pub = pubkey.save_pkcs1()
pubfile = open('daepublic.pem','wb')
pubfile.write(pub)
pubfile.close()

pri = privkey.save_pkcs1()
prifile = open('daeprivate.pem','wb')
prifile.write(pri)
prifile.close()

