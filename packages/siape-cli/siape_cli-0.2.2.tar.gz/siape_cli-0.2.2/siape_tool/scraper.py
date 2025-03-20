import time
import pandas as pd
import requests
import warnings

from tqdm import tqdm

from siape_tool.utils.constants import *
from tenacity import retry, wait_exponential, stop_after_attempt

from siape_tool.utils.errors import NotAdmissibleYearRange
warnings.filterwarnings("ignore")


class ScraperSIAPE:
    def __init__(
        self, 
        resid=None, 
        nzeb=None,
        year_emission_lower=None,
        year_emission_upper=None
        ):
        self.url = URL
        self.headers = HEADERS
        self.resid = RESID_MAP_IN[resid] if resid is not None else None
        self.nzeb = nzeb
        self.year_epc = self._create_year_epc(year_emission_lower, year_emission_upper)

    def get_data(self, payload):
        """
        Get the data for the climatic zones
        :param payload:
        :return:
        """
        self._prepare_payload(payload)
        self._get_responses()
        self._convert_to_df()

        return self.dfs.apply(pd.to_numeric, errors='ignore')

    def _prepare_payload(self, payload):
        filters = {}
        if self.resid is not None:
            filters["where[destuso]"] = self.resid
        if self.nzeb is not None:
            filters["where[nzeb]"] = "true"
        if self.year_epc is not None:
            self._check_years_within_range(self.year_epc)
            filters["where[annoape][range][]"] = self.year_epc

        self.payloads = [
            {**single_payload, **filters} for single_payload in payload
        ]
        
    def _get_responses(self):
        """
        Get the responses from the API
        :return:
        """
        if isinstance(self.payloads, dict):
            self.payloads = [self.payloads]

        responses = []

        @retry(
            wait=wait_exponential(multiplier=1, min=4, max=10), 
            stop=stop_after_attempt(3)
            )
        def _make_request(single_payload):
            response = requests.request(
                "POST", 
                self.url, 
                headers=self.headers, 
                data=single_payload
                )
            response.raise_for_status()
            return response

        for i, single_payload in enumerate(tqdm(self.payloads), 1):
            try:
                response = _make_request(single_payload)
                responses.append(response)
            except requests.RequestException as e:
                print(f"Failed to get response for payload {i}: {e}")
                responses.append(None)

            if i % 10 == 0:
                time.sleep(1)  # THIS SEEMS TO BE THE OPTIMAL COMBO

        self.responses = responses

    def _convert_to_df(self):
        dfs = []
        dictionary = dict(zip(self.responses, self.payloads))

        for response, input in dictionary.items():
            df_response = self._create_df_response(response)
            df_response = self.apply_cla_eng_order(df_response)
            df_input = self._create_df_input(input)
            print(df_input.to_markdown())
            df_merged = self._merge_df_input_response(df_input, df_response)

            dfs.append(df_merged)

        self.dfs = pd.concat(dfs, ignore_index=True)
        self.dfs = self._final_cleaning(self.dfs)
    
    def _create_year_epc(self, year_emission_lower, year_emission_upper):
        if year_emission_lower is not None and year_emission_upper is not None:
            return [year_emission_lower, year_emission_upper]
        elif year_emission_lower is not None and year_emission_upper is None:
            return [year_emission_lower, 1000000000]
        elif year_emission_lower is None and year_emission_upper is not None:
            return [-1000000000, year_emission_upper]
        else:
            return None
        
    def _check_years_within_range(self, year_epc):
        if year_epc[0] > year_epc[1]:
            raise NotAdmissibleYearRange(
                f"Year filter {year_epc[0]} is greater than year filter {year_epc[1]}"
            )
        
        if year_epc[0] == year_epc[1]:
            raise NotAdmissibleYearRange(
                f"Year filter {year_epc[0]} is equal to year filter {year_epc[1]}"
            )
        
        if (year_epc[0] != -1_000_000_000 and year_epc[0] < 2015) or (year_epc[1] < 2015):
            raise NotAdmissibleYearRange(
                f"Year filter {year_epc[0]} or {year_epc[1]} is less than 2015"
            )


    @staticmethod
    def apply_cla_eng_order(df):
        df['CLA_ENG'] = pd.Categorical(
            df['CLA_ENG'], categories=ENERGETIC_CLASSES_ORDERED, ordered=True
        )

        df.sort_values("CLA_ENG", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def _create_df_input(self, input):
        return pd.DataFrame([input])

    def _create_df_response(self, response):
        if response.json()["data"] == []:
            return pd.DataFrame(
                {
                    "APE": [0],
                    "CLA_ENG": [0],
                    "EP_GL_NREN": [0],
                    "EP_GL_REN": [0],
                    "CO2": [0]
                }
            )
        else:
            df = pd.DataFrame(response.json()["data"])
            df.columns = ['# OBS', 'CLA_ENG', 'EP_GL_NREN', 'EP_GL_REN', 'CO2']
            return df

    def _merge_df_input_response(self, df_input, df_response):
        df = pd.concat([df_input, df_response], axis=1)
        fill_values = self._create_fill_values(df)
        df.fillna(fill_values, inplace=True)
        return df

    def _final_cleaning(self, dfs):
        """
        Remove columns that have always the same value, maps the remaining column with a dict.
        :param dfs:
        :return:
        """
        dfs.drop(columns=["group[]", "nofilter"], inplace=True)

        dfs = dfs.rename(columns={
            "where[annoc][range][]": "YEAR_RANGE",
            "where[suris][range][]": "SURFACE_RANGE",
            "where[zoncli]": "ZON_CLI",
            "where[destuso]": "RESID",
            "where[cod_reg]": "REG",
            "where[cod_pro]": "PROV",
            "where[annoape][range][]": "YEAR_EPC",
        })

        if "RESID" in dfs.columns:
            dfs["RESID"] = dfs["RESID"].map(RESID_MAP_OUT)

        if "REG" in dfs.columns:
            dfs["REG"] = dfs["REG"].map(CODREG_TO_REG)

        if "PROV" in dfs.columns:
            dfs["PROV"] = dfs["PROV"].map(CODPROV_TO_PROV)

        return dfs

    def _create_fill_values(self, df):
        fill_values = df.iloc[0, :-5].to_dict()
        fill_values = {key: str(value) for key, value in fill_values.items()}

        return fill_values
