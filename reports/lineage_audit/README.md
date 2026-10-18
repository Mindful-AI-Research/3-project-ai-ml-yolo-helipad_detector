## [Auditoria de linhagem: de onde vieram os arquivos]()

<br><br>

> Detecção visual automatizada baseada em imagem, sujeita a erros e não equivalente a validação operacional, legal, de segurança ou aeronáutica. Esta pasta trata da linhagem dos dados, não da validação de locais.

<br><br>

## [Origem dos arquivos]()

<br>

### [***Inventário de campo***]()

`field_tiles_inventory.csv` e `field_tiles_inventory_raw.csv` foram **reconstituídos dos arquivos compactados** `src/geospatial/mosaic_*/mosaic_*.zip` (ramo `main`, revisão `9e767ec1f8d711b4e09f920aadf802c3855acb9a`). O inventário principal tem 7.767 linhas (pares região × *tile*, igual ao conjunto histórico) e 5.540 identificadores de *tile* distintos; o `raw` guarda as 8.083 entradas brutas dos zips.

<br>

### [***Imagens anotadas***]()

`train_valid_test_tiles_overlap.csv` cobre as 226 imagens de `data/training/exp1` (revisão `bc5a0ad953e4ffc8433d3e3f68d245068ebddc5a`), cujo conteúdo é idêntico ao de `data/training/exp2` e ao da pasta `My-First-Project-2` do repositório de Pedro Vyctor Almeida (versão 2 do conjunto: 178 treino, 34 validação, 14 teste).

<br>

### [***Resumo e critérios***]()

`overlap_summary.json` reúne critérios, denominadores e totais usados em `docs/evidence/relatorio_evidencias_exp1_exp2.docx`.

<br><br>

## [Colunas principais]()

<br>

### [***field_tiles_inventory.csv***]()

`tile_id`, `original_name`, `region_folder`, `z`, `x`, `y`, `path_in_zip`, `zip_files`, `n_copies_in_zips`, `copies_identical_crc`, `size_bytes`, `crc32`, `n_regions_with_tile`.

<br>

### [***train_valid_test_tiles_overlap.csv***]()

`split`, `original_name`, `name_tile_id`, `name_id_shared_by_n_images`, `pixel_best_field_tile`, `pixel_mae256`, `pixel_match_le5`, `resolved_tile_id`, `resolved_by`, `z`, `x`, `y`, `in_field_exact`, `field_regions`, `min_chebyshev_to_field`, `field_within_1/2/3/5`, `train_same_tile_id`, `train_min_chebyshev`.

<br><br>

## [Critérios]()

<br>

### [***Como ler os números***]()

- **Cópia por pixel:** erro absoluto médio (0–255) menor ou igual a 5 entre a imagem anotada e o *tile* de campo mais parecido (pré-filtro 32×32, medida em 256×256). Todas as coincidências ficam em 1,56 ou menos; nenhuma outra fica abaixo de 16,9.
- **Identificador pelo nome:** z/x/y lidos do nome do arquivo; não é confiável quando várias imagens compartilham o mesmo nome de *tile* (23 imagens do Itaim Bibi).
- **Vizinhança:** distância de Chebyshev em *tiles* z19 (cerca de 70 m, aproximação). Vizinho não é vazamento confirmado.

<br><br>

## [Limitações e pendências]()

<br>

### [***O que não está coberto***]()

- Cópias giradas, recortadas, reescaladas ou de outra data não são detectadas pelo critério de pixel.
- Não há detecções por *tile* nos materiais, então o efeito da sobreposição nas taxas de campo não foi calculado.
- Faltam 176 *tiles* da Faria Lima no inventário (840 no histórico contra 664 distintos nos zips), e a divisão da Av. Paulista desloca 5 *tiles*.
- Os scripts que geraram estes arquivos ainda não estão versionados: **Desconhecido nos materiais fornecidos.** Sem eles, os números não são reproduzíveis por terceiros; recomenda-se versioná-los em `src/geospatial/` antes de citá-los como reprodutíveis.
