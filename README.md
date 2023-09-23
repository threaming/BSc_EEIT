# Bachelor Electrical Engineering :zap:

Summaries and notes of my bachelor of electrical engineering and information technology at [HSLU](https://www.hslu.ch/de-ch/technik-architektur/ueber-uns/organisation/institute/technik/elektrotechnik/). The summaries are a mix between English and German, but are mostly written in German.

## Tools used

The majority of all the summaries are written using [Quarto](https://quarto.org/). It's neato and I've used it for quite some time.

## Template used

All of the document formats are written by me. If you want to use the template, it's inside `template/summary`.

## `cmbright`

When using the TinyTex-Distribution (which is just a smaller TexLive with less packages), the `cmbright` package doesn't work with specific configuration (I think it has something to do with the `multicol` package), giving out an *auto expansion* error.

What worked for me was to install following packages manually...

- `cm-super`
- `fontspec`
- `hfbright`

..., run `updmap` in the terminal and afterwards set the quarto-setting in the document.
```yaml
fontenc: T1
```

It does give a nicer text body (using *CM Bright Light*) and feels nice to look at.

# Credits

Alot of the hard work (e.g. setting up the templates) has been done by

- [@joelvonrotz](https://github.com/joelvonrotz)