# The Digital Borderline (Reg-Track LatAm)

An interactive dashboard that compares how Mexico, Colombia and Argentina regulate streaming platforms.

It scores each country on four factors (taxes, local content quotas, sanctioning power and ease of operating) and combines the first three into a single "Digital Rigidity Index" (IRD). The weights of the index are adjustable from the sidebar, so the reader can see how the ranking changes with different priorities.

**Status: prototype.** The figures are working estimates written directly in `app.py`; they are not yet linked to legal sources. Treat them as illustrative until a sourced dataset replaces them.

## What it shows

- An IRD score per country, recalculated live as the weights change
- A radar chart of each country's regulatory profile
- A short regulatory note per country
- The main regulators and tax authorities in each country

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Built with

Python, Streamlit, pandas and Plotly.

---

## En español

Tablero interactivo que compara la regulación de las plataformas de streaming en México, Colombia y Argentina.

Califica a cada país en cuatro factores (impuestos, cuotas de contenido local, poder sancionador y facilidad operativa) y combina los tres primeros en un "Índice de Rigidez Digital" (IRD). Las ponderaciones se ajustan desde la barra lateral.

**Estado: prototipo.** Las cifras son estimaciones de trabajo escritas en `app.py`; todavía no están ligadas a fuentes legales.
