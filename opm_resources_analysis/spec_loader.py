from opm_resources_analysis.utils import load_specs


class SpecLoader:
    df_hero = load_specs('Hero')

    df_configs = load_specs('Configs')
    df_configs = df_configs.rename(columns={'Unnamed: 2': 'Key'})

    @classmethod
    def get_config_value(cls, key):
        return cls.df_configs.loc[cls.df_configs['Key'] == key, 'Value'].values[0]

    @classmethod
    def get_seven_day_reward(cls, day):
        rewards = cls.get_config_value('SevenDayReward').split('#S#')[day - 1]


