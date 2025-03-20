# pn-sequence

> A Python library for testing pseudo-noise (PN) sequences

## Install

## Developing

```bash
poetry install
eval $(poetry env activate)
python

# Inside REPL
import pn_sequence
pn_sequence.is_first_postulate_true("011001000111101") # etc.
```

## Testing

```bash
poetry run pytest
```

For coverage:

```bash
poetry run pytest --cov=pn_sequence tests/
```

## Contributing

Contributions are welcome. Please fork the project and use feature a feature branch. For bugs and suggestions, please open an issue.

## License

The project is licensed under the GNU Lesser General Public License. See [LICENSE](/LICENSE) for full terms.

## References

1. Menezes, A.J., Van Oorschot, P.C. and Vanstone, S.A. (2018) Handbook of Applied Cryptography. 1st edn. CRC Press. Available at: https://doi.org/10.1201/9780429466335.
2. Pinaki, M. (no date) ‘Golomb’s Randomness Postulates’. Available at: https://www.iitg.ac.in/pinaki/Golomb.pdf.
