
import csv
import logging
import os

ICGC_SAMPLE_ID_KEY="ICGC Submitted Sample ID"
SEQUENCING_STRATEGY_KEY='ICGC Submitted Sequencing Strategy'
EGAF_ACCESSION_KEY='EGA File Accession'
DELIMITER='\t'

class EGAAudit:

    def __init__(self, csv_file):
        self._csv_file = open(csv_file,'r')
        self._rows = []
        self._load_csv()
        return

    def _load_csv(self):
        csv_reader = csv.DictReader(self._csv_file, delimiter=DELIMITER)
        for row in csv_reader:
            self._rows.append(row)

    def get_ids(self, seq_strategy=None):
        ids = []
        for row in self._rows:
            if seq_strategy != None:
                if row['ICGC Submitted Sequencing Strategy'] == seq_strategy:
                    ids.append({'ICGC_SAMPLE_ID_KEY':row[ICGC_SAMPLE_ID_KEY],'SEQUENCING_STRATEGY_KEY':row[SEQUENCING_STRATEGY_KEY],'EGAF_ACCESSION_KEY':row[EGAF_ACCESSION_KEY]})
            else:
                ids.append({'ICGC_SAMPLE_ID_KEY':row[ICGC_SAMPLE_ID_KEY],'SEQUENCING_STRATEGY_KEY':row[SEQUENCING_STRATEGY_KEY],'EGAF_ACCESSION_KEY':row[EGAF_ACCESSION_KEY]})
        return ids

    def get_row(self,icgc_sample_id, egaf, seq_strategy):
        for row in self._rows:
            if row[ICGC_SAMPLE_ID_KEY] == icgc_sample_id and row[SEQUENCING_STRATEGY_KEY] == seq_strategy and row[EGAF_ACCESSION_KEY] == egaf:
                return row
        raise Exception("There is no row found with the following informations: icgc_sample_id=%s, egafid=%s, seq_strategy=%s" % (icgc_sample_id, egaf, seq_strategy))

    def _get_key(self, icgc_sample_id, egaf, seq_strategy, key):
        self._csv_file.seek(0)
        row = self.get_row(icgc_sample_id, egaf, seq_strategy)
        return  row[key]

    def get_egaf_id(self, icgc_sample_id, egaf, seq_strategy):
        return self._get_key(icgc_sample_id, egaf, seq_strategy,EGAF_ACCESSION_KEY)

    def get_egaf_ids(self, ids=[]):
        if len(ids) == 0:
            ids = self.get_ids()
        fids = []
        for id in ids:
            logging.debug("EGAFID added: %s" % (id))
            fids.append(self.get_egaf_id(id['ICGC_SAMPLE_ID_KEY'],id['EGAF_ACCESSION_KEY'],id['SEQUENCING_STRATEGY_KEY']))
        return fids

    def find_rows(self, egaf_id):
        self._csv_file.seek(0)
        rows = []
        csv_reader = csv.DictReader(self._csv_file, delimiter=DELIMITER)
        for row in csv_reader:
            if row[EGAF_ACCESSION_KEY] == egaf_id:
                rows.append(row)
        return rows

    def get_job(self, egaf_id, metadata_repo):
        job = {}
        rows = self.find_rows(egaf_id)

        job['bundle_id'] = self._get_bundle_id(rows[0]['EGA Analysis Accession'],rows[0]['EGA Run Accession'])
        job['name'] = job['bundle_id']
        job['bundle_type'] = self._get_bundle_type(rows[0]['EGA Analysis Accession'],rows[0]['EGA Run Accession'])
        job['donor_gender'] = rows[0] if rows[0]["Donor Gender"] in ['male','female'] else 'unspecified'
        job['ega_analysis_id'] = rows[0]['EGA Analysis Accession']
        job['ega_dataset_id'] = rows[0]["EGA Dataset Accession"]
        job['ega_experiment_id'] = rows[0]["EGA Experiment Accession"]
        job['ega_metadata_file_name'] = 'bundle.'+job['bundle_id']+'.xml'
        job['ega_metadata_repo'] = metadata_repo
        job['ega_run_id'] = rows[0]["EGA Run Accession"]
        job['ega_sample_id'] = rows[0]["EGA Sample Accession"]
        job['ega_study_id'] = rows[0]["EGA Study Accession"]
        job['insert_size'] = rows[0]["Insert Size"]
        job['library_strategy'] = rows[0][SEQUENCING_STRATEGY_KEY]
        job['paired_end'] = rows[0]["Paired-End"]
        job['project_code'] = rows[0]["ICGC DCC Project Code"]
        job['reference_genome'] = rows[0]["Reference Genome"]
        job['submitter'] = rows[0]["ICGC DCC Project Code"]
        job['submitter_donor_id'] = rows[0]["ICGC Submitted Donor ID"]
        job['submitter_sample_id'] = rows[0]["ICGC Submitted Sample ID"]
        job['submitter_specimen_id'] = rows[0]["ICGC Submitted Specimen ID"]
        job['submitter_specimen_type'] = rows[0]["ICGC Submitted Specimen Type"]

        job['files'] = []
        for row in rows:
            file = {}
            file['ega_file_id'] = row[EGAF_ACCESSION_KEY]
            file['file_md5sum'] = row['Unencrypted Checksum']
            file['file_name'] = row['Unencrypted Checksum']+'.'+os.path.basename(row['EGA Raw Sequence Filename'][:-4] if str(row['EGA Raw Sequence Filename']).endswith('.gpg') else row['EGA Raw Sequence Filename'])
            file['size'] = row['File Size']
            job['files'].append(file)

        return ".".join(['job',job['bundle_id'],job['project_code'],job['submitter_sample_id'],job['ega_sample_id']]),job

    def _get_bundle_type(self, analysis_accession, run_accession):
        if analysis_accession != None and analysis_accession != "":
            return "analysis"
        if run_accession != None and run_accession != "":
            return "run"
        return None

    def _get_bundle_id(self, analysis_accession, run_accession):
        if analysis_accession != None and analysis_accession != "":
            return analysis_accession
        if run_accession != None and run_accession != "":
            return run_accession
        return None

    def get_info_from_egafid(self, egafid, *args):
        row = self.find_rows(egafid)[0]
        return [row[x] for x in args]

