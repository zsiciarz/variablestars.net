from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Star",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "constellation",
                    models.CharField(
                        db_index=True,
                        max_length=3,
                        verbose_name="Constellation",
                        choices=[
                            ("AND", "Andromeda"),
                            ("ANT", "Antlia"),
                            ("APS", "Apus"),
                            ("AQR", "Aquarius"),
                            ("AQL", "Aquila"),
                            ("ARA", "Ara"),
                            ("ARI", "Aries"),
                            ("AUR", "Auriga"),
                            ("BOO", "Bo\xf6tes"),
                            ("CAE", "Caelum"),
                            ("CAM", "Camelopardalis"),
                            ("CNC", "Cancer"),
                            ("CVN", "Canes Venatici"),
                            ("CMA", "Canis Major"),
                            ("CMI", "Canis Minor"),
                            ("CAP", "Capricornus"),
                            ("CAR", "Carina"),
                            ("CAS", "Cassiopeia"),
                            ("CEN", "Centaurus"),
                            ("CEP", "Cepheus"),
                            ("CET", "Cetus"),
                            ("CHA", "Chamaeleon"),
                            ("CIR", "Circinus"),
                            ("COL", "Columba"),
                            ("COM", "Coma Berenices"),
                            ("CRA", "Corona Australis"),
                            ("CRB", "Corona Borealis"),
                            ("CRV", "Corvus"),
                            ("CRT", "Crater"),
                            ("CRU", "Crux"),
                            ("CYG", "Cygnus"),
                            ("DEL", "Delphinus"),
                            ("DOR", "Dorado"),
                            ("DRA", "Draco"),
                            ("EQU", "Equuleus"),
                            ("ERI", "Eridanus"),
                            ("FOR", "Fornax"),
                            ("GEM", "Gemini"),
                            ("GRU", "Grus"),
                            ("HER", "Hercules"),
                            ("HOR", "Horologium"),
                            ("HYA", "Hydra"),
                            ("HYI", "Hydrus"),
                            ("IND", "Indus"),
                            ("LAC", "Lacerta"),
                            ("LEO", "Leo"),
                            ("LMI", "Leo Minor"),
                            ("LEP", "Lepus"),
                            ("LIB", "Libra"),
                            ("LUP", "Lupus"),
                            ("LYN", "Lynx"),
                            ("LYR", "Lyra"),
                            ("MEN", "Mensa"),
                            ("MIC", "Microscopium"),
                            ("MON", "Monoceros"),
                            ("MUS", "Musca"),
                            ("NOR", "Norma"),
                            ("OCT", "Octans"),
                            ("OPH", "Ophiuchus"),
                            ("ORI", "Orion"),
                            ("PAV", "Pavo"),
                            ("PEG", "Pegasus"),
                            ("PER", "Perseus"),
                            ("PHE", "Phoenix"),
                            ("PIC", "Pictor"),
                            ("PSC", "Pisces"),
                            ("PSA", "Piscis Austrinus"),
                            ("PUP", "Puppis"),
                            ("PYX", "Pyxis"),
                            ("RET", "Reticulum"),
                            ("SGE", "Sagitta"),
                            ("SGR", "Sagittarius"),
                            ("SCO", "Scorpius"),
                            ("SCL", "Sculptor"),
                            ("SCT", "Scutum"),
                            ("SER", "Serpens"),
                            ("SEX", "Sextans"),
                            ("TAU", "Taurus"),
                            ("TEL", "Telescopium"),
                            ("TRI", "Triangulum"),
                            ("TRA", "Triangulum Australe"),
                            ("TUC", "Tucana"),
                            ("UMA", "Ursa Major"),
                            ("UMI", "Ursa Minor"),
                            ("VEL", "Vela"),
                            ("VIR", "Virgo"),
                            ("VOL", "Volans"),
                            ("VUL", "Vulpecula"),
                        ],
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=20, verbose_name="Name", db_index=True),
                ),
                (
                    "ra",
                    models.CharField(
                        default="", max_length=15, verbose_name="Right Ascension"
                    ),
                ),
                (
                    "dec",
                    models.CharField(
                        default="", max_length=15, verbose_name="Declination"
                    ),
                ),
                (
                    "max_magnitude",
                    models.FloatField(null=True, verbose_name="Maximum brightness"),
                ),
                (
                    "min_magnitude",
                    models.FloatField(null=True, verbose_name="Minimum brightness"),
                ),
                ("epoch", models.FloatField(null=True, verbose_name="Epoch")),
                ("period", models.FloatField(null=True, verbose_name="Period")),
                (
                    "observations_count",
                    models.PositiveIntegerField(default=0, editable=False),
                ),
            ],
            options={
                "ordering": ("constellation", "name"),
                "verbose_name": "Variable star",
                "verbose_name_plural": "Variable stars",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="VariabilityType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=12, verbose_name="Letter code", db_index=True
                    ),
                ),
                (
                    "short_description",
                    models.CharField(
                        default="",
                        max_length=100,
                        verbose_name="Short description",
                        blank=True,
                    ),
                ),
                (
                    "long_description",
                    models.TextField(default="", verbose_name="Long description"),
                ),
            ],
            options={
                "ordering": ("code",),
                "verbose_name": "Variability type",
                "verbose_name_plural": "Variability types",
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="star",
            name="variability_type",
            field=models.ForeignKey(
                verbose_name="Type of variability",
                blank=True,
                to="stars.VariabilityType",
                null=True,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
    ]
