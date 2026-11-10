# Propuesta: gentle-design-skill — calidad de diseño profesional para Gentle Shell

**Autor:** comunidad Gentle Programming · **Licencia:** MIT · **Estado:** implementado y verificado
**Repo:** `github.com/Reaan06/gentle-design-skill` · **Hub:** `gentlemanprogramming.com/gentle-hub` (topics `gentle-shell-package` + `gentle-shell-skill`)

## 1. El problema

Los agentes de código generan interfaces que se reconocen al instante como "hechas por IA": gradientes violeta, Inter en todo, tres cards idénticas, bordes redondeados uniformes, cero estados de error. La causa tiene nombre — **convergencia distributiva**: ante prompts sin dirección, el modelo regresa a la mediana estadística de todo lo que ya vio. El resultado es el look de *vibe coding*: técnicamente correcto, genérico de más.

Las herramientas profesionales de diseño con IA (Vercel v0, Google Stitch, Figma Make) no tienen ese problema porque **no le dejan la decisión de gusto al azar**: congelan tokens antes de generar, prohiben clichés con alternativas nombradas, y revisan el render antes de entregar.

## 2. La propuesta

**`gentle-design-skill`**: una skill acompañante para el workflow de `gentle-design` en Gentle Shell que codifica, como reglas mecánicas y con evidencia citada, cómo funcionan por dentro esos harnesses profesionales. No es un prompt bonito: es un sistema de reglas verificables + un gate ejecutable.

Qué aporta sobre el stack existente:

- **Dirección antes que tokens**: catálogo de 8 direcciones de arte nombradas + Direction Contract (tesis, presupuesto de color, movimientos prohibidos). Rompe la convergencia antes de escribir una línea de CSS.
- **Foundation Pass**: bloque de tokens semánticos (3–5 colores, rampa 4px, escala tipográfica documentada, un solo `--radius`) — el mismo mecanismo que Stitch separa del prompt de generación.
- **Craft Pass**: disciplina de color (~90% superficies neutras), textura en vez de decoración, matriz completa de estados, motion <300ms con `prefers-reduced-motion`.
- **Professional Gate**: checklist mecánica de ~40 ítems + **`design-gate.py`**, un linter estático de 12 reglas (tokens, rampa, `transition: all`, tells de slop) con salida `file:line` y exit code — el "design-slop cop" que convierte el gusto en evidencia.
- **Cobertura Web / Mobile / Desktop**: convenciones iOS/Material, densidad y teclado de desktop, dark mode de primera clase.
- **DESIGN.md**: cada diseño aprobado emite su sistema de tokens en la spec de Google (`@google/design.md lint`), portable entre harnesses.

## 3. El método: ingeniería inversa perfecta

Nada es "opinión de modelo". Cada regla cita su evidencia (E1–E10 en `references/evidence.md`):

| Evidencia | Fuente |
| --- | --- |
| Tema shadcn capturado en runtime (monocromo, bordes 1px, radius 10px) | `ui.shadcn.com`, computo de estilos en vivo |
| Landings de v0 y Stitch (restricción, tipografía display, textura) | capturas de pantalla analizadas |
| "All states designed", "never `transition: all`" | Vercel design guidelines |
| Tokens congelados antes de generar; 3 variantes por defecto | repos oficiales `google-labs-code/stitch-skills` |
| Linter de 11 reglas + WCAG 4.5:1 | `google-labs-code/design.md` |
| Dos pasadas + crítica con screenshots | `anthropics/skills` (frontend-design) |
| Autofixers deterministas; 57% menos fallos con design.md | blog de ingeniería de Vercel |
| Test de sustitución, tesis visual, alternativas nombradas | skills públicos anti-slop (impeccable, anti-slop-design, unslop-ui) |
| Los "tells" mecánicos del slop | design-slop cop (checks DOM/CSS deterministas) |

Los prompts filtrados de v0/Lovable se usan solo como pistas y están marcados como no verificados.

## 4. Resultados verificados

- **Pulse** (SaaS de analítica): landing web 1440×900, vista mobile 390×844, workspace desktop 1440×900 + variantes dark — 86/86 checks estructurales, gate limpio, DESIGN.md lint limpio (0 errores), paridad geométrica entre temas.
- **Molino** (tostador editorial): diseñado desde un Direction Contract congelado; el test de sustitución falla como debe — la etiqueta de tueste impresa y el índice foliado solo pueden ser de un tostador. Gate exit 0, lint exit 0, acento gastado exactamente 3 veces por vista.
- El gate detectó y corrigió un hallazgo real (stencil de máscara sin token) en su primera pasada sobre arte existente.

## 5. Costo y alcance

- Skill estática: 1 SKILL.md + 9 referencias + 1 script Python (stdlib). Sin dependencias nuevas, sin servicios externos.
- Se integra al workflow existente (gentle-design entrega, gentle-ui-design UX, esta skill agrega el oficio visual).
- Mantenimiento: la evidencia está fechada; el gate es determinista y testeable.

## 6. Pedido

Publicar el repo bajo los topics del Hub (`gentle-shell-package`, `gentle-shell-skill`) para que aparezca en el catálogo comunitario, y — si el equipo lo considera — promocionarlo como ejemplo del patrón "skill con evidencia + gate ejecutable" en la documentación de la comunidad.
