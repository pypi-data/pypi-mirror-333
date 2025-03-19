import click
from dicomdiff.main import compare_dicom_files, print_differences


@click.group()
def cli():
    pass


@cli.command()
@click.argument("original_file")
@click.argument("deidentified_file")
def compare(original_file, deidentified_file):
    differences = compare_dicom_files(original_file, deidentified_file)
    print_differences(differences)


if __name__ == "__main__":
    cli()
