# Document Engine

Block 1C adds the first real document layer.

## Components

- `DocumentReader`
- `DocumentBlock`
- `StyleReader`
- `PageIterator`

## Principle

The document layer only reads Word content. It does not decide what is a tax row.
That decision belongs to the row classifier in a later block.

## Run

```bash
python run.py --word "path\to\Taxestruktur.docx"
```
