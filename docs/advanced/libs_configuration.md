# FIFT AND FUNC LIBS CONFIGURATION
We decided to not update your local copies ot these libs automatically because you can change them according to your needs. But if we update these libs we will notify you with warning:
```
Its seems that your local fift and func libs differs from their actual versions.
```
You will have 2 options to remove this warning:
1. Update your local copies of libs with command `toncli update_libs`
2. Remove the warning by adding additional parameter (or changing existing parameter) `LIBS_WARNING=False`