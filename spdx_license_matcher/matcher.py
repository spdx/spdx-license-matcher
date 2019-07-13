import click

from .computation import get_close_matches, get_matching_string
from .difference import generate_diff, get_similarity_percent
from .utils import colors, get_spdx_license_text


@click.command()
@click.option('--text_file', '-f', type=click.File('r'), help='File in which there is the text you want to match against the SPDX License database.'
         'If not provided, a prompt will allow you to type the input text.')
@click.option('--threshold', '-t', default=0.9, type = click.FloatRange(0.0, 1.0), help='Confidence threshold below which we just won"t consider it a match.', show_default=True)
@click.option('--limit', '-l', default=0.99, type=click.FloatRange(0.9, 1.0), help='Limit at which we will consider a match as a perfect match.', show_default=True)
def matcher(text_file, threshold, limit):
    """SPDX License matcher to match license text against the SPDX license list using an algorithm which finds close matches. """
    if text_file:
        inputText = text_file.read()
    else:
        inputText = click.prompt('Enter a text', type=str)

    inputText = bytes(inputText, 'utf-8').decode('unicode-escape')
    matches = get_close_matches(inputText, threshold, limit)
    matchingString = get_matching_string(matches, limit, inputText)
    if matchingString == '':
        licenseID = max(matches, key=matches.get)
        spdxLicenseText = get_spdx_license_text(licenseID)
        similarityPercent = get_similarity_percent(spdxLicenseText, inputText)
        click.echo(colors('\nThe given license text matches {}% with that of {} based on Levenstein distance.'.format(similarityPercent, licenseID), 94))
        differences = generate_diff(spdxLicenseText, inputText)
        for line in differences:
            if line[0] == '+':
                line = colors(line, 92)
            if line[0] == '-':
                line = colors(line, 91)
            if line[0] == '@':
                line = colors(line, 90)
            click.echo(line)
    else:
        click.echo(colors(matchingString, 92))


if __name__ == "__main__":
    matcher()
