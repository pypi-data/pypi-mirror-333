[![](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mbujosab/nacallib/master?filepath=doc%2FNotebooks%2FNotebook.ipynb)
[![](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mbujosab/nacal-Jupyter-Notebooks/master)

# Módulo "NAcAL" (Notación Asociativa para un Curso de Álgebra Lineal)

Este módulo implementa la notación, los objetos y los procedimientos
descritos en el
[libro](https://mbujosab.github.io/CursoDeAlgebraLineal/libro.pdf) del
[Curso de ÁLgebra
Lineal](https://github.com/mbujosab/CursoDeAlgebraLineal)
correspondiente a la asignatura [Matemáticas
II.](https://www.ucm.es/fundamentos-analisis-economico2/algebra-2)

Aunque es posible su uso desde un terminal, este módulo está pensado
para ser empleado en [Notebooks de Jupyter](https://jupyter.org/) (y
también desde documentos de LaTeX).

Este módulo muestra cómo llegar a la mayoría de los resultados del curso
de Álgebra Lineal empleando el método de eliminación. NAcAL no solo
resuelve sistemas de ecuaciones, invierte matrices, calcula
determinantes, diagonaliza matrices tanto por semejanza como por
congruencia, etc. sino que muestra los pasos empleados para llegar al
resultado como si se hiciera con lápiz y papel (ofreciendo el código
LaTeX para expresar todo el proceso). También permite trabajar con
subespacios vectoriales y espacios afines (bases, sistemas generadores,
ecuaciones cartesianas y paramétricas, complementos ortogonales,
interseción, pertenecia, etc.). También puede trabajar de manera
simbólica, pues emplea los objetos básicos del módulo
[Sympy](https://www.sympy.org/en/index.html).

La documentación explica la programación del código y sirve como
material adicional al [libro del
curso](https://github.com/mbujosab/CursoDeAlgebraLineal) (este módulo es
una implementación literal de lo mostrado en dicho libro).

Puede ver el uso del módulo sin necesidad de instalar nada, tan solo
accediendo a los Notebooks de Jupyter alojados en
[![](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mbujosab/nacal-Jupyter-Notebooks/master)
con su navegador de páginas web (tenga en cuenta que MyBinder puede
tardar unos minutos en cargar el módulo y el Notebook de demostración).

## Instalación

[nacal](https://pypi.org/project/nacal/) funciona con Python \>=3.6.
Puede instalar el paquete desde PyPI via pip:

``` bash
pip3 install nacal
```

[nacal](https://pypi.org/project/nacal/) emplea
[Sympy](https://www.sympy.org/en/index.html). Para instalar Sympy:

``` bash
pip3 install sympy
```

## Uso

Para emplear este módulo en una consola de Python, una vez instalada:

``` bash
pyhton3
>>> from nacal import *
```

Para emplearlo en un Notebook de Jupyter, ejecute en un "Cell" de código

``` example
from nacal import *
```

## Desinstalación

Para desinstalar [nacal](https://pypi.org/project/nacal/):

``` bash
pip3 uninstall nacal
```
