"""Collects metadata of assemblies from NCBI API"""

__author__ = "Berger, Phillip"

from time import sleep

import requests

from loguru import logger


class NCBIAssemblyMetadata:
    """Class to collect metadata of assemblies from the NCBI API."""

    _all_metadata: dict
    _count: int
    _parameters: dict
    _accessions: list[str]
    _contig_n50: int
    _all_metadata_complete: dict

    def __init__(self, all_metadata: dict, count=8, contig_n50=10000):
        self._all_metadata = all_metadata
        self._count = count
        self._contig_n50 = contig_n50

        self._set_parameters()

        tmp_metadata = {}
        for tax_id, curr_metadata in self._all_metadata.items():
            sleep(2)
            species_name = curr_metadata["sci_name"]
            logger.info("Collecting metadata of {name}", name=species_name)
            accessions = self._make_request(taxon=tax_id)
            if len(accessions) != 0:
                curr_metadata["accessions"] = accessions
                tmp_metadata[tax_id] = curr_metadata

        self._all_metadata_complete = tmp_metadata

    def _set_parameters(self):
        params = {
            "filters.reference_only": "false",
            "filters.assembly_source": "refseq",
            "filters.exclude_atypical": "true",
            "page_size": self._count,
            "page_token": "",
        }
        params_ref = params.copy()
        params_ref["filters.reference_only"] = "true"

        params_comp_genome = params.copy()
        params_comp_genome["filters.assembly_level"] = "complete_genome"

        params_chrom = params.copy()
        params_chrom["filters.assembly_level"] = "chromosome"

        params_scaffold = params.copy()
        params_scaffold["filters.assembly_level"] = "scaffold"

        params_contig = params.copy()
        params_contig["filters.assembly_level"] = "contig"

        self._parameters = {
            "params_ref": params_ref,
            "params_comp_genome": params_comp_genome,
            "params_chrom": params_chrom,
            "params_scaffold": params_scaffold,
            "params_contig": params_contig,
        }

    def _make_request(self, taxon: str):
        api_url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/{taxon}/dataset_report"
        accessions = []
        count = 0
        for request_type, parameters in self._parameters.items():
            raw_response = requests.get(api_url, params=parameters, timeout=5)
            response = raw_response.json()
            if response:
                try:
                    reports = response["reports"]
                    for report in reports:
                        accession = report["accession"]
                        contig_n50 = report["assembly_stats"]["contig_n50"]
                        taxonomy_check_status = report["average_nucleotide_identity"][
                            "taxonomy_check_status"
                        ]
                        if count < self._count:
                            if (
                                taxonomy_check_status == "OK"
                                and contig_n50 > self._contig_n50
                            ):
                                accessions.append(accession)
                                count += 1
                        else:
                            break
                except KeyError:
                    logger.debug(
                        "While requesting: {type} an error response was given",
                        type=request_type,
                    )
                    logger.debug(str(response))

            if count >= self._count:
                break
        return accessions

    def get_all_metadata(self):
        """Returns all metadata of the assemblies."""
        return self._all_metadata_complete
