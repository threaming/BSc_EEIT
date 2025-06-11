# Assignment crypto 01

Author: Andreas Ming
Time Spent: 2h

The attached XTEA encryption/decryption script is based on a script found online (source mentioned in script) and was extended to be used with flexible length text and terminal support.

The implementation was straight forward and the encryption worked. Issues arouse when we tried to decypher other teams encrypted texts and we didn't get anything readable. It turned out, that the issue was due to teams handling the file formats differently. Some used binary, where others saved in HEX format. It turned out that a big part in standardising such encryption systems is also how the data are handled outside the algorithm.

A area for improvement in my solution could be the automatic random key generation. Currently a key has to be supplied for encryption, but for sakes of security it would make sense to generate a new random key along every new encryption cycle.