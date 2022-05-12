
USE Group_F;
DROP TABLES IF EXISTS Damage;
DROP TABLES IF EXISTS Mortality;
DROP TABLES IF EXISTS Growth;
DROP TABLES IF EXISTS Biomass;
DROP TABLES IF EXISTS Location;
DROP TABLES IF EXISTS Tree;
DROP TABLES IF EXISTS Species;


create table Species (
    SPCD integer not null, -- Species code
    COMMON_NAME VARCHAR(100), --  Common name 
    GENUS VARCHAR(40), -- Genus 
    SPECIES VARCHAR(50), -- Species (Latin) 
    VARIETY VARCHAR(50), -- Variety 
    SUBSPECIES VARCHAR(50), -- Subspecies 
    SPECIES_SYMBOL VARCHAR(8), -- Species symbol

    primary key (SPCD)
)engine=InnoDB;

create table Tree (
    ID integer not null auto_increment, -- tree id because primary key needs to be unique
    TREE integer not null, -- TREE IDENTIFIER
    CN integer(13) not null, -- Sequence number. A unique sequence number used to identify a tree record
    SPCD integer not null, -- SPECIES CODE
    DIA integer, -- CURRENT DIAMETER
    HT integer, -- TREE HEIGHT
    TPA_UNADJ integer, -- Trees per acre unadjusted.
    TPAMORT_UNADJ integer, -- Mortality trees per acre per year unadjusted.
    TPAREMV_UNADJ integer, -- Removal trees per acre per year unadjusted.
    TPAGROW_UNADJ integer, -- Growth trees per acre unadjusted. 
    CCLCD integer, -- Crown class code
    UNCRCD integer(3), -- Uncompacted live crown ratio
    CPOSCD integer(2), -- Crown position code
    CLIGHTCD integer(2), -- Crown light exposure code
    CVIGORCD integer(2), -- Crown vigor code (sapling)
    CDENCD integer(3), -- Crown density code 
    CDIEBKCD integer(3), -- Crown dieback code
    CREATED_DATE date, --
    MODIFIED_DATE date, --
    
    foreign key (SPCD) references Species (SPCD),
    primary key (ID),
    INDEX tree_idx (TREE)
)engine=InnoDB;

create table Location (
    LOCID integer not null auto_increment, -- LOCATION IDENTIFIER
    -- LAT integer, -- LATITUDE
    -- LON integer, -- LONGITUDE
    STATECD integer, -- STATE CODE
    INVYR YEAR, -- INVENTORY YEAR
    UNITCD integer, -- UNIT CODE
    COUNTYCD integer, -- COUNTY INDETIFICATION NUMBER
    PLOT integer, -- PLOT ID OR PLOT NUMBER
    SUBP integer,
    TREEID integer not null, -- FOREIGN KEY TREE ID

	-- foreign key (TREEID) references Tree (ID),
    primary key (LOCID),
    INDEX yr_plot (INVYR, PLOT)
)engine=InnoDB;

create table Biomass (
    BIOID integer not null auto_increment, -- BIOMASS IDENTIFIER
    DRYBIO_BOLE integer, -- DRY BIOMASS IN THE MERCHANTABLE BOLE
    DRYBIO_TOP integer, -- DRY BIOMASS IN THE TOP AND LIMBS OF THE TREE
    DRYBIO_STUMP integer, -- DRY BIOMASS IN THE TREE STUMP
    DRYBIO_SAPLING integer, -- Aboveground dry biomass of saplings.
    DRYBIO_WDLD_SPP integer, -- Aboveground dry biomass of woodland tree species. 
    DRYBIO_BG integer, -- Belowground dry biomass.
    CARBON_AG integer, -- Aboveground carbon.
    CARBON_BG integer, -- Belowground carbon. 

    TREEID integer not null, -- FOREIGN KEY TREE ID

	-- foreign key (TREEID) references Tree (ID),
    primary key (BIOID)
)engine=InnoDB;

create table Growth (
    GROWID integer not null auto_increment, -- GROWTH IDENTIFIER
    GROWCFGS integer, -- Net annual merchantable cubic-foot growth of a growing-stock tree on timberland.
    GROWBFSL integer, -- Net annual merchantable board-foot growth of a sawtimber tree on timberland
    GROWCFAL integer, -- Net annual sound cubic-foot growth of a live tree on timberland 
    DIA_BEGIN integer, --
    DIA_MIDPT integer, -- 
    DIA_END integer, -- 
    ANN_DIA_GROWTH integer, -- 
    HT_BEGIN integer, -- 
    HT_MIDPT integer, -- 
    HT_END integer, --  
    ANN_HT_GROWTH integer, --
    TREEID integer not null, -- FOREIGN KEY TREE ID

	-- foreign key (TREEID) references Tree (ID),
    primary key (GROWID)
)engine=InnoDB;

create table Mortality (
    MORID integer not null auto_increment, -- MORTALITY IDENTIFIER
    MORTCFGS integer, -- Merchantable cubic-foot volume of a growing-stock tree for mortality purposes on timberland
    MORTBFSL integer, -- Merchantable board-foot volume of a sawtimber tree for mortality purposes on timberland
    MORTCFAL integer, -- Sound cubic-foot volume of a tree for mortality purposes on timberland
    AGENTCD integer, -- Cause of death (agent) code.
    TREEID integer not null, -- FOREIGN KEY TREE ID

    -- foreign key (TREEID) references Tree (ID),
    primary key (MORID)
)engine=InnoDB;

create table Damage (
    DAMID integer not null auto_increment, -- DAMAGE IDENTIFIER
    DAMLOC1 integer, -- Damage location 1
    DAMTYP1 integer, -- Damage type 1
    DAMSEV1 integer, -- Damage severity 1
    DAMLOC2 integer, -- Damage location 2
    DAMTYP2 integer, -- Damage type 2
    DAMSEV2 integer, -- Damage severity 2
    DECAYCD integer, -- Decay class code
    TREEID integer, -- FOREIGN KEY TREE ID
    
    -- foreign key (TREEID) references Tree (ID),
    primary key (DAMID)
)engine=InnoDB;