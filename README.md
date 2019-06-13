# Ab Urbe Condita

A small program to convert times and dates into the Roman system.

Call `auc.py` with the following arguments:

```
--help      shows this help text
--now       convert current date and time
--custom    convert a custom date (ISO 8601)
--simple    only print the Roman format
```

For example:
```
python auc.py --now
    23:27, Thursday, 13 June 2019 AD
    hora II post solis occasum, dies Iovis, Idus Junii MMDCCLXXII AUC
```

To use a custom date, you must use the ISO 8601 format, for example:
```
python auc.py --custom 1234-05-06
    06 May 1234 AD
    dies Saturni, diem II ante Nonas Maii MCMLXXXVII AUC
```

