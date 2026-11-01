# Figuras em TikZ / TikZ figures

Compile / Compilar (LaTeX com `tikz`, `helvet`, `amsmath`):

```bash
# PT: \def\LANG{p}  ·  EN: \def\LANG{e}
pdflatex -jobname=fig1_pt '\def\LANG{p}\input{fig1}'
pdflatex -jobname=fig1_en '\def\LANG{e}\input{fig1}'
pdftocairo -svg fig1_pt.pdf fig1_pt.svg
```

Saída em `assets/figures/` / Output in `assets/figures/`.
