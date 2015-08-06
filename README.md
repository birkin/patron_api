### Overview

For a few purposes, we access data from our [iii-millennium](http://iii.com/products/millennium) patron-api.

The response that comes back is html and the data elements are simply strings. JSON would be much more useful.

This code converts the patron-api string output into nice json hash elements.

The service is used internally, so no demo link is provided. But to give an example, instead of raw patron-api output like:

```
<HTML><BODY>
...
PATRN NAME[pn]=Demolast, Demofirst<BR>
P BARCODE[pb]=1 2222 33333 4444<BR>
...
</BODY></HTML>
```

...it instead returns:

```
{
    "patron_name": {
        "label": "PATRN NAME",
        "code": "pn",
        "value": "Demolast, Demofirst" },
    "patron_barcode": {
        "label": "P BARCODE",
        "code": "pb",
        "value": "1 2222 33333 4444",
        "converted_value": "12222333334444" }
}
```

---