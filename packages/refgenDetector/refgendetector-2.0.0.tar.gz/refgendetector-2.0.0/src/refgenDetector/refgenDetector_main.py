#!/usr/bin/env python

""" refgenDetector.py: Script to infer the reference genome used to create a BAM or CRAM"""

__author__ = "Mireia Marin Ginestar"
__version__ = "2.0"
__maintainer__ = "Mireia Marin Ginestar"
__email__ = "mireia.marin@crg.eu"
__status__ = "Developement"

version = "2.0.0"

import os
import sys
# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from refgenDetector.reference_genome_dictionaries import *
from refgenDetector.exceptions.NoFileException import *
import argparse
import csv
import gzip
import pysam
import psutil
import time
from rich.console import Console

console = Console()

def monitor_resources(func):
    def wrapper(*args, **kwargs):
        process = psutil.Process()
        start_time = time.time()
        start_cpu_time = process.cpu_times()

        # Run the function
        result = func(*args, **kwargs)

        end_time = time.time()
        end_cpu_time = process.cpu_times()
        duration = end_time - start_time

        # Calculate CPU time
        cpu_user = end_cpu_time.user - start_cpu_time.user
        cpu_system = end_cpu_time.system - start_cpu_time.system
        total_cpu_time = cpu_user + cpu_system

        # Get memory usage (current RSS in MB)
        memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB

        # Get disk I/O
        io_counters = process.io_counters()
        bytes_read = io_counters.read_bytes
        bytes_written = io_counters.write_bytes

        # Print results
        print(f"Execution time: {duration:.2f} seconds")
        print(f"CPU time used: {total_cpu_time:.2f} seconds")
        print(f"Memory usage (RSS): {memory_usage:.2f} MB")
        if bytes_read > (1024*1024):
            print(f"Disk I/O - Read: {bytes_read / (1024 * 1024):.2f} MB, Written: {bytes_written / (1024 * 1024):.2f} MB")
        elif bytes_read > 1024:
            print(f"Disk I/O - Read: {bytes_read / (1024):.2f} KB, Written: {bytes_written / (1024):.2f} KB")
        else:
            print(f"Disk I/O - Read: {bytes_read:.2f} Bytes, Written: {bytes_written:.2f} Bytes")

        return result

    return wrapper

def intersection_targetfile_referencerepo(dict_SN_LN, reference_genome):
    """
    Find the matches between the target file and the repository of unique contigs per reference genome.
    Returns the actual matches (ln info) instead of just their count.
    Args:
         dict_SN_LN (dict) : dictionary with the contig (SN: key, LN: value) info from the target file
         reference_genome (dict entry): one of the versions from major_releases

    Returns:
        matches (set) : list of lengths matching to the version currently being read
        reference_genome["build"] (str): build of the version currently being read
        reference_genome["species"] (str): specie of the version currently being read
    """
    matches = set(dict_SN_LN.values()).intersection(reference_genome["ref_gen"].values())
    return matches, reference_genome["build"], reference_genome["species"]

def check_if_decoy(matches_info, target_file):
    """
    Checks if there's inconsistency of the versions in the target file or if the multiple matches are random
    Args:
         matches_info (list): list of tuples. Each tuple have 3 positions: lengths from the contigs matching,
         version where the contigs match, specie from the version.
         target_file (str): path of the target file

    Returns:
        If the matches to the secondary version are at least as long as the shortest chromosome of the version with
        more matches then a message raising the incosistency is printed.
        If the matches to the secondary version are shorter than the shortest chromosome then it assumes it's a decoy
        contig matching another version randomly and returns:
        incosistency = False so the code can continue in comparison() and give the results based on the version with
        most matches.
    """
    incosistency_found = False
    filtered_entries = [entry for entry in matches_info if entry[0]]  # get the multiple matches
    match = max(filtered_entries, key=lambda ref_gen_w_macthes: len(ref_gen_w_macthes[0]))  # version with most
    # matches with LN values
    inconsistency_matches = []
    for version in filtered_entries:
        if version != match:
            for ln in version[0]:
                if int(ln) > min_values[match[1]]: # checks if the ln matching is more or less chr length
                    ref_dict = globals().get(version[1])
                    inconsistency_matches.extend([key for key, value in ref_dict.items() if value == ln])
                    incosistency_found = True
            if incosistency_found == True:
                console.print(f"[bold]File:[/bold] {target_file} \n[bold][red]Error:[/bold] Inconsistency found "
                              f"- file contains contigs from different genome versions[/red]")
                console.print(f"[red]Contigs {inconsistency_matches} belong to {version[1]}, but the rest belongs to"
                              f" {match[1]}[/red].")
    return incosistency_found


def comparison(dict_SN_LN, target_file):
    """
    First, it defines the major release to which the header belongs to. Then, checks if a flavor can be inferred.
    Args:
         dict_SN_LN (dict): dictionary with the contig (SN: key, LN: value) info from the target file
         target_file (str): path of the target file

    Returns:
        Prints the file path being analyzed,the specie and the reference genome version inferred.
        It raises an error if:
            - The contigs in the target file are not in the database (a specie or ref gen version not included in the tool)
            - There are contigs belonging to more than one release/specie. This will be printed if the match between
            species is as long as the shortest chromosome from the version with the most matches. If the match is
            shorter it assumes it's a random match e.g a decoy contig that randomly matches the length of
            another species/version.
    """

    matches_info = [intersection_targetfile_referencerepo(dict_SN_LN, major_releases[ref]) for ref in major_releases]
    matches_with_counts = [(len(matches), build, species) for matches, build, species in matches_info]
    max_match = max(matches_with_counts, key=lambda ref_gen_w_macthes: ref_gen_w_macthes[0]) # Find the major release
    # with the maximum matches
    incosistency = False

    # check all the matches belong to the same release version
    multiple_matches = []
    for match in matches_with_counts:
        if match[0] != 0:
            multiple_matches.append(match)

    if len(multiple_matches) > 1 :
        if multiple_matches[0][1] != "hg17" and multiple_matches[1][1] != "hg18": # these versions share contig lengths
            if multiple_matches[0][1] != "rhemac3" and multiple_matches[1][1] != "rhemac8":
                incosistency = check_if_decoy(matches_info, target_file)

    if incosistency == False:

        if max_match[0] == 0:
            console.print(f"[bold]File:[/bold] {target_file} \n[bold][red]Reference genome can't be inferred[/bold] - "
                          "The contigs in the file are not found in refgenDetector database[red]")

        elif max_match[1] == "GRCh37": #check for GRCh37 flavors

            matches_flavors = [
                intersection_targetfile_referencerepo(dict_SN_LN, flavors_GRCh37[ref])
                for ref in flavors_GRCh37
            ]

            match_flavors = max(matches_flavors, key=lambda x: x[0])
            if match_flavors: #if some flavor was defined it prints it
                console.print(f"[bold]File:[/bold] {target_file} \n[bold]Specie detected:[/bold] {match_flavors[2]} "
                f"[bold]\nReference genome version:[/bold] {match_flavors[1]}")
            else: #if there wasnt any flavor inferred, the major release it printed
                console.print(f"[bold]File:[/bold] {target_file} \n[bold]Specie detected:[/bold] Homo sapiens \n["
                              f"bold]Reference genome version:[/bold] GRCh37")

        elif max_match[1] == "GRCh38": #checks for GRCh38 flavors

            if any("HLA-" in key for key in dict_SN_LN.keys()):
                #first checks if the contigs contain in their names HLA-
                console.print(f"[bold]File:[/bold] {target_file} \n[bold]Specie detected:[/bold] Homo sapiens \n[bold]"
                              f"Reference genome version:[/bold] hs38DH_extra")
            elif set(dict_SN_LN.values()).intersection(verily_difGRCh38.values()):#checks if the Verily's unique
                # lengths are present
                console.print(f"[bold]File:[/bold] {target_file} \n[bold]Specie detected:[/bold] Homo sapiens \n[bold]"
                              f"Reference genome version:[/bold] GRCh38_no_alt_plus_hs38d1")
            else: # if no GRCh38 flavor is inferred, the major release is printed
                console.print(f"[bold]File:[/bold] {target_file} \n[bold]Specie detected:[/bold] Homo sapiens \n["
                              f"bold]Reference genome version:[/bold] GRCh38")
        else: # print the major releases with no considered flavors.
            console.print(f"[bold]File:[/bold] {target_file} \n[bold]Specie detected:[/bold] {match[2]} "
                  f"\n[bold]Reference genome version:[/bold] {match[1]}")




def get_info_bamcram(header_bam_cram, target_file, md5, assembly):
    """
    Second function of the BAM/CRAM module. Loop over the SQ (sequence dictionary) records in the header, creates a
    dictionary with the contigs names and lengths, if present and requested by the user (adding -m and -a in the
    argument) prints AS and M5

    Args:
        header_bam_cram(pysam.libcalignmentfile.AlignmentHeader): text object

    Returns:
        dict_SN_LN (dict): dictionary with the contig (SN: key, LN: value) info from the target file
        target_file (str): path of the target file
        dict_assembly[1] (str): if present and asked by the user, AS value from the target file header
        dict_M5 (dict): if present and asked by the user, M5 values from the target file header
    """

    dict_SN_LN = {sq_record["SN"]: sq_record["LN"] for sq_record in header_bam_cram.get("SQ", [])}

    if assembly: # if the user chose -a
        dict_assembly = set(sq_record["AS"] for sq_record in header_bam_cram.get("SQ", []) if "AS" in sq_record)
        if dict_assembly:
            console.print(f"[bold]AS field:[/bold] {dict_assembly.pop()}")
    if md5: # if the user chose -m
        dict_M5 = set(sq_record["M5"] for sq_record in header_bam_cram.get("SQ", []) if "M5" in sq_record)
        if dict_M5:
            console.print(f"[bold]M5 fields:[/bold]{dict_M5}")
    comparison(dict_SN_LN, target_file)


def process_data_bamcram(target_file, md5, assembly):
    """
    First function of the BAM/CRAM module. It opens each BAM or CRAM provided by the user and extracts the header.

    Args:
        target_file (str): path to the file

    Returns:
        header_bam_cram (pysam.libcalignmentfile.AlignmentHeader): text object
    """
    try:
        save = pysam.set_verbosity(0)  # https://github.com/pysam-developers/pysam/issues/939
        bam_cram = pysam.AlignmentFile(target_file, "rb")
        pysam.set_verbosity(save)
    except Exception as e:
        console.print(f"[bold]File:[/bold] {target_file} \n[bold][red]Error:[/bold][red] {e.__class__}, {e}")

    header_bam_cram = bam_cram.header
    get_info_bamcram(header_bam_cram, target_file, md5, assembly)

def get_info_txt(header_txt, md5, assembly):
    """
    Second function of the txt module. Extracts the SQ (sequence dictionary) records in the header, creates a
    dictionary with the contigs names and lengths, and, if present and requested by the user (adding -m and -a in the
    argument) prints AS and M5.

    Args:
        header_txt (io.TextIOWrapper): text object

    Returns:
        dict_SN_LN (dict): dictionary with the contig (SN: key, LN: value) info from the target file
        header_txt.name (str): path of the target file
        dict_assembly[1] (str): if present and asked by the user, AS value from the target file header
        dict_M5 (dict): if present and asked by the user, M5 values from the target file header
    """
    header_reader = csv.reader(header_txt, delimiter="\t")
    dict_SQ = [line for line in header_reader if "@SQ" in line]
    try:
        dict_SN_LN = {line[1].replace("SN:", ""): int(line[2].replace("LN:", "")) for line in
           dict_SQ}  #the dictonary values must be int due to the structure of the collection of reference dictionaries
    except ValueError:
        print(f"Check the LN field of your header {header_txt.name} only contains numbers")

    comparison(dict_SN_LN, header_txt.name)

    if assembly:  # # if the user chose -a
        dict_assembly = [l for line in dict_SQ for l in line if "AS" in l][:1]
        if dict_assembly:  # if AS is present in the header
            console.print(f"[bold]AS field:[/bold] {dict_assembly[0].split(':')[1]}")
    if md5:  # # if the user chose -m
        for i in dict_SQ[0]:
            if "M5" in i:
                dict_M5 = {line[1].replace("SN:", ""): i.replace("M5:", "") for line in
                      dict_SQ}
                console.print(f"[bold]MD5 fields:[/bold] {dict_M5}")

def process_data_txt(target_file, md5, assembly):
    """
    First function of the txt module. It opens each header in --path. gzip or uncompressed and encoded in utf-8 or
    iso-8859-1.

    Args:
        target_file (str): path to the file

    Returns:
        header_txt (io.TextIOWrapper): text object
    """
    try:
        if os.path.isfile(target_file):
            with open(target_file, "r") as header_txt:
                get_info_txt(header_txt, md5, assembly)
        else:
            raise NoFileException()
    except UnicodeError:
        with open(target_file, "r", encoding="iso-8859-1") as header_txt:
            get_info_txt(header_txt, md5, assembly)
    except OSError:
        try:
            with gzip.open(target_file, "rt") as header_txt:
                get_info_txt(header_txt, md5, assembly)
        except UnicodeError:
            with gzip.open(target_file, "rt", encoding="iso-8859-1") as header_txt:
                get_info_txt(header_txt, md5, assembly)
    except NoFileException:
        console.print(f"[bold]File:[/bold] {target_file} \n[bold][red]Error:[/bold][red] The path provided is not "
                      f"found or you are using the incorrect --type option.")
    except Exception as e:
        print("Unexpected error:\n", e)



@monitor_resources
def main():
    """
    Process the users inputs and chooses to run BAM/CRAM module or txt module, depending on the -t argument

    Args:
        --path (txt): List of files to process [MANDATORY]
        --type (BAM/CRAM or Headers): type of files that are stated in --path [MANDATORY]
        --md5 (flag): if present the md5 values from the ref gen will be printed [OPTIONAL]
        --as (flag): if present the AS will be printed [OPTIONAL]

    Returns:
        if --type = BAM/CRAM calls process_data_bamcram()
        if --type = Headers calls process_data_txt()
    """
    parser = argparse.ArgumentParser(prog="INFERRING THE REFERENCE GENOME USED TO ALIGN BAM OR CRAM FILE")
    #MANDATORY ARGUMENTS
    parser.add_argument("-p", "--path", help="Path to main txt. It will consist of paths to the files to be "
                                             "analyzed (one path per line).",
                        required=True)
    parser.add_argument("-t", "--type", choices=["BAM/CRAM", "Headers"],
                        help="All the files in the txt provided in --path must be BAM/CRAMs or headers in a txt. "
                             "Choose -t depending on the type of files you are going to analyze.", required=True)
    #OPTIONAL ARGUMENTS
    parser.add_argument("-m", "--md5", required=False, action="store_true",
                        help="[OPTIONAL] If you want to obtain the md5 of the contigs present in the header, "
                             "add --md5 to your command. This will print the md5 values if the field M5 was present in "
                             "your header.")
    parser.add_argument("-a", "--assembly", required=False, action="store_true",
                        help="[OPTIONAL] If you want to obtain the assembly declared in the header add --assembly "
                             "to your command. This will print the assembly if the field AS was present in "
                             "your header.")
    args = parser.parse_args()
    print(f"* Running refgenDetector {version} *")
    try:
        with open(args.path,"r") as txt:
            if args.type == "Headers":
                for target_file in txt:
                    console.print("[bold]---[/bold]")
                    process_data_txt(target_file.strip(), args.md5, args.assembly)

            else:
                for target_file in txt:
                    console.print("[bold]---[/bold]")
                    process_data_bamcram(target_file.strip(), args.md5, args.assembly)
            console.print("[bold]---[/bold]")
    except OSError:
        console.print(f"[red]The file {args.path} provided in --path can't be opened. Make sure to include the path "
                      f"to a txt file formed by paths to headers saved in txts or to BAM/CRAMs files (one per line)[/red]"
                      f"\nRun [bold]refgenDetector -h[/bold] to get more information about the usage of the tool."
                      f"\n---")



if __name__ == "__main__":  # the first executed function will be main()
    main()
