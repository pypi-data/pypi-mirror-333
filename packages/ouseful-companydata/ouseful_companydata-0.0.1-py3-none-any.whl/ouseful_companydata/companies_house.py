import json
import base64
from urllib.parse import urlencode
import requests
from time import sleep
import os
import sqlite3
import networkx as nx

import chart_studio.plotly as py
import plotly.graph_objects as go


class CompaniesHouseAPI:
    BASE_URL = "https://api.companieshouse.gov.uk"

    def __init__(
        self,
        api_token=None,
        db=None,
        initialize_tables=True,
        use_cache=False,
        cache_name="companies_house_cache",
        cache_expire_after=3600,
        cache_backend="sqlite",
    ):
        self.api_token = api_token
        self.db = None
        self.create_db(db, initialize_tables)

        self.session = None

        # Set up the session with or without caching
        if use_cache:
            import requests_cache

            self.session = requests_cache.CachedSession(
                cache_name=cache_name,
                backend=cache_backend,
                expire_after=cache_expire_after,
            )
            print(f"Caching enabled with {cache_backend} backend: {cache_name}")
        else:
            self.session = requests.Session()
            print("Caching disabled")

        # Hacks for now
        # self.cosparsed = []

    def set_api_token(self, api_token):
        """Set the API token after initialization"""
        self.api_token = api_token

    def _url_nice_req(self, url, headers=None, timeout=300):
        """Makes a request with rate limiting handling"""
        try:
            return requests.get(url, headers=headers, timeout=timeout)
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, "status_code") and e.response.status_code == 429:
                print("Overloaded API, resting for a bit...")
                time.sleep(timeout)
                return self._url_nice_req(url, headers=headers)
            else:
                # Re-raise other errors
                raise

    def _request(self, url, args=None):
        """Make an authenticated request to the Companies House API"""
        if self.api_token is None:
            raise ValueError(
                "API token not set. Use set_api_token() or initialize with an API token."
            )

        if args is not None:
            url = "{}?{}".format(url, urlencode(args))

        # Prepare headers with Basic Auth
        base64string = base64.b64encode(f"{self.api_token}:".encode("utf-8")).decode(
            "utf-8"
        )
        headers = {"Authorization": f"Basic {base64string}"}

        response = self._url_nice_req(url, headers=headers)

        if response is None or not response.ok:
            print(f"Oops: {url}, {response}")
            return None

        return response.json()

    def create_db(self, db=None, initialize_tables=True):
        """
        Initialize the database for storing company/director information.

        Parameters:
        - db: Can be one of:
            - None: Creates an in-memory database
            - str: Path to a database file (existing or new)
            - sqlite3.Connection: Existing database connection
        - initialize_tables: If True, creates/recreates tables. If False, assumes tables exist

        Returns:
        - sqlite3.Connection object
        """
        # Close existing connection if any
        if self.db is not None:
            self.db.close()

        # Handle different input types
        if db is None:
            # Create in-memory database
            self.db = sqlite3.connect(":memory:")
            # Always initialize tables for in-memory databases
            initialize_tables = True
        elif isinstance(db, str):
            # Check if it's an existing file (and not empty)
            file_exists = os.path.isfile(db) and os.path.getsize(db) > 0

            # Create file-based database
            self.db = sqlite3.connect(db)

            # If file exists and initialize_tables=False, assume structure is already set up
            if file_exists and not initialize_tables:
                return self.db
        elif isinstance(db, sqlite3.Connection):
            # Use existing connection
            self.db = db
            # If initialize_tables=False, assume structure is already set up
            if not initialize_tables:
                return self.db
        else:
            raise TypeError(
                "db must be None, a string filepath, or a sqlite3.Connection object"
            )

        print("Database created.")
        # Only initialize tables if requested
        if initialize_tables:
            self._initialize_tables()

        return self.db

    def _initialize_tables(self):
        """Create the database schema"""

        print("Creating database tables.")
        # Set up cursor
        c = self.db.cursor()

        # Drop existing tables if they exist
        tables = ["directorslite", "companieslite", "codirs", "coredirs", "singlecos"]
        for table in tables:
            c.execute(f"DROP TABLE IF EXISTS {table}")

        # Create tables
        c.execute(
            """create table directorslite
                (dirnum text primary key,
                dirdob integer,
                dirname text)"""
        )

        c.execute(
            """create table companieslite
                (conum text primary key,
                costatus text,
                coname text)"""
        )

        c.execute(
            """create table codirs
                (conum text,
                dirnum text,
                typ text,
                status text)"""
        )

        c.execute(
            """create table coredirs
                (dirnum text)"""
        )

        c.execute(
            """create table singlecos
                (conum text)"""
        )

        # Commit changes
        self.db.commit()

    def get_cosparsed_in_dblite(self):
        if self.db is None:
            raise ValueError("Database not initialized. Call create_db() first.")

        c = self.db.cursor()
        c.execute("SELECT conum FROM singlecos")

        # Extract just the company numbers as a simple list
        return [row[0] for row in c.fetchall()]

    def get_dirsparsed_in_dblite(self):
        """If we've processed a director, keep track of them.


        Returns:
        - List of director numbers
        """
        if self.db is None:
            raise ValueError("Database not initialized. Call create_db() first.")

        c = self.db.cursor()
        c.execute("SELECT dirnum FROM coredirs")

        # Extract just the company numbers as a simple list
        return [row[0] for row in c.fetchall()]

    def get_director_numbers_in_dblite(self):
        """
        Get list of all director numbers stored in the database

        Returns:
        - List of director numbers
        """
        if self.db is None:
            raise ValueError("Database not initialized. Call create_db() first.")

        c = self.db.cursor()
        c.execute("SELECT dirnum FROM directorslite")

        # Extract just the company numbers as a simple list
        return [row[0] for row in c.fetchall()]

    def get_company_numbers_in_dblite(self):
        """
        Get list of all company numbers stored in the database

        Returns:
        - List of company numbers
        """
        if self.db is None:
            raise ValueError("Database not initialized. Call create_db() first.")

        c = self.db.cursor()
        c.execute("SELECT conum FROM companieslite")

        # Extract just the company numbers as a simple list
        return [row[0] for row in c.fetchall()]

    def ch_getCompanyCharges(self, cn, n=50, start_index=""):
        url = f"{self.BASE_URL}/company/{cn}/charges"
        properties = {"items_per_page": n, "start_index": ""}
        c = self._request(url, properties)
        return c  # May return None

    def ch_disqualifiedOfficer(self, slug):
        url = f"{self.BASE_URL}/{slug}".format()
        return self._request(url)

    def ch_disqualifiedNaturalOfficer(self,o):
        url = f"{self.BASE_URL}/disqualified-officers/natural/{o}"
        return self._request(url)

    def ch_disqualifiedCorporateOfficer(self,o):
        url = f"{self.BASE_URL}/disqualified-officers/corporate/{o}"
        return self._request( url)

    def ch_searchDisQualifiedOfficers(self, q, n=5, start_index="", company="", locality=""):
        """
        Search for disqualified directors.
        
        Also add a filter to firther limit the response to directors by locality.
        """
        url = f"{self.BASE_URL}/search/disqualified-officers"
        properties = {"q": q, "items_per_page": n, "start_index": start_index}
        o = self._request(url, properties)
        if company != "":
            o["items"] = [
                j
                for j in o["items"]
                for i in self.ch_disqualifiedOfficer(j["links"]["self"])["disqualifications"]
                for k in i["company_names"]
                if company.lower() in k.lower()
            ]
        if locality != "":
            o["items"] = [
                j
                for j in o["items"]
                if locality.lower() in j["address"]["locality"].lower()
            ]
        return o

    def get_psc(self, company_record):
        """
        Get persons of significant control from Company Record.
        """
        if (
            "links" in company_record
            and "persons_with_significant_control" in company_record["links"]
        ):
            return (
                company_record["company_name"],
                company_record["company_number"],
                company_record["links"]["persons_with_significant_control"],
            )
        return (
            company_record["company_name"],
            company_record["company_number"],
            "no psc",
        )

    def ch_getCompany(self, cn):
        """
        Get company details from company number.

        Parameters:
        - cn: The company number.

        Returns:
        - JSON response from the API
        """
        url = f"{self.BASE_URL}/company/{cn}"
        return self._request(url)

    def ch_getCompanyPSC(self, cn):
        url = f"https://api.company-information.service.gov.uk/company/{cn}/persons-with-significant-control"
        return self._request(url)

    def ch_search_companies(
        self, query, items_per_page=50, start_index="", search_type=None
    ):
        """
        Search for companies by name

        Parameters:
        - query: The company name to search for
        - items_per_page: Number of results to return per page
        - start_index: Index to start from for pagination
        - search_type: Filter type - "exact", "contains", or None

        Returns:
        - JSON response from the API, filtered according to search_type
        """
        url = f"{self.BASE_URL}/search/companies"
        properties = {
            "q": query,
            "items_per_page": items_per_page,
            "start_index": start_index,
        }

        results = self._request(url, properties)

        if results is None:
            return results

        if search_type == "contains":
            results["items"] = [
                i for i in results["items"] if query.lower() in i["title"].lower()
            ]
        elif search_type == "exact":
            results["items"] = [
                i for i in results["items"] if query.lower() == i["title"].lower()
            ]

        return results

    def ch_getCompanyOfficers(self, cn, typ="all", role="all"):
        # typ: all, current, previous
        url = f"{self.BASE_URL}/company/{cn}/officers"
        co = self._request(url)
        if typ == "current":
            co["items"] = [i for i in co["items"] if "resigned_on" not in i]
            # should possibly check here that len(co['items'])==co['active_count'] ?
        elif typ == "previous":
            co["items"] = [i for i in co["items"] if "resigned_on" in i]
        if role != "all":
            co["items"] = [i for i in co["items"] if role == i["officer_role"]]
        return co

    def ch_searchOfficers(self, name, n=50, start_index="", company="", exact=None):
        url = f"{self.BASE_URL}/search/officers"
        properties = {"q": name, "items_per_page": n, "start_index": start_index}
        o = self._request(url, properties)

        if o is None:
            return o

        if exact == "forename":
            # This isn't right e.g. double barrelled surnames
            s = name.lower().split(" ")
            o["items"] = [
                i
                for i in o["items"]
                if i["title"].lower().split(" ")[0] == s[0]
                and i["title"].lower().split(" ")[-1] == s[-1]
            ]
        elif exact == "fullname":
            o["items"] = [i for i in o["items"] if i["title"].lower() == name.lower()]
        if company != "":
            for p in o["items"]:
                p["items"] = [
                    i
                    for i in self.ch_getAppointments(p["links"]["self"])["items"]
                    if company.lower() in i["appointed_to"]["company_name"].lower()
                ]
            o["items"] = [i for i in o["items"] if len(i["items"])]
        return o

    def ch_getAppointments(self, slug, location=None, typ="all", role="all"):
        if len(slug.split("/")) == 1:
            slug = f"/officers/{slug}/appointments"
        url = f"{self.BASE_URL}{slug}"
        a = self._request(url)

        if a is None:
            return None

        if location is not None:
            a["items"] = [
                i
                for i in a["items"]
                if location.lower() in i["address"]["locality"].lower()
            ]
        if typ == "current":
            a["items"] = [i for i in a["items"] if "resigned_on" not in i]
            a["items"] = [
                i
                for i in a["items"]
                if "company_status" in i["appointed_to"]
                and i["appointed_to"]["company_status"] == "active"
            ]
            # should possibly check here that len(co['items'])==co['active_count'] ?
        elif typ == "previous":
            a["items"] = [i for i in a["items"] if "resigned_on" in i]
        elif typ == "dissolved":
            a["items"] = [
                i
                for i in a["items"]
                if "company_status" in i["appointed_to"]
                and i["appointed_to"]["company_status"] == "dissolved"
            ]

        if role != "all":
            a["items"] = [i for i in a["items"] if role == i["officer_role"]]
        return a

    def dirCompanySeeds(self, dirseeds, typ="all", role="all"):
        """Find companies associated with dirseeds"""
        companyseeds = []
        for d in dirseeds:
            for c in self.ch_getAppointments(d, typ=typ, role=role)["items"]:
                companyseeds.append(c["appointed_to"]["company_number"])
        return companyseeds

    def get_director_company_data(
        self, name="", dirseeds=None, role="all", typ="current"
    ):
        """Grab data for a director's company network.
        Optionally limit the director role (e.g. 'director', 'Finance Director')
        """
        dirseeds, companyseeds = self.get_dirSeedsCompanySeeds(name, dirseeds)
        for seed in companyseeds:
            self.updateOnCo(seed, typ=typ, role=role)

    def get_dirSeedsCompanySeeds(
        self,
        name="",
        dirseeds=None,
    ):
        """Given a director and or set of director seeds, find all the associated companies."""
        dirseeds = [] if dirseeds is None else dirseeds
        if name:
            for d in self.ch_searchOfficers(name, n=10, exact="forename")["items"]:
                dirseeds.append(d["links"]["self"])

        companyseeds = self.dirCompanySeeds(dirseeds, typ="current", role="director")

        return dirseeds, companyseeds

    def updateOnCo(self, seed, typ="current", role="director"):
        """
        Find codirectors of a director, and the other companies they direct.
        """
        print("harvesting {}".format(seed))

        # A form of cacheing - don't pull down data we already have
        dirsdone = self.get_director_numbers_in_dblite()
        cosdone = self.get_company_numbers_in_dblite()
        _dirsparsed = self.get_dirsparsed_in_dblite()

        # These are the directors parsed in this function call
        dirsparsed = []

        c = self.db.cursor()

        # apiNice()

        # Get the company officers for the provided comnpany number
        o = self.ch_getCompanyOfficers(seed, typ=typ, role=role)["items"]

        # Extract core directory information
        x = [
            {
                "dirnum": p["links"]["officer"]["appointments"]
                .strip("/")
                .split("/")[1],
                "dirdob": p["date_of_birth"]["year"] if "date_of_birth" in p else None,
                "dirname": p["name"],
            }
            for p in o
        ]

        # z keeps track of fresh director records
        z = []
        # Make a note of each officer retrieved
        for y in x:
            if y["dirnum"] not in dirsdone:
                z.append(y)
                dirsdone.append(y["dirnum"])
            if isinstance(z, dict):
                z = [z]
        print("Adding {} directors".format(len(z)))
        # And add that director to the db
        c.executemany(
            "INSERT INTO directorslite (dirnum, dirdob,dirname)"
            "VALUES (:dirnum,:dirdob,:dirname)",
            z,
        )

        # For each of the officers, get the companies they are appointed to
        for oo in [
            i
            for i in o
            if i["links"]["officer"]["appointments"].strip("/").split("/")[1]
            not in set(dirsparsed) | set(_dirsparsed)
        ]:
            oid = oo["links"]["officer"]["appointments"].strip("/").split("/")[1]
            print("New director: {}".format(oid))
            # apiNice()
            ooo = self.ch_getAppointments(oid, typ=typ, role=role)
            # apiNice()
            # Play nice with the api
            sleep(0.5)
            # add company details
            x = [
                {
                    "conum": p["appointed_to"]["company_number"],
                    "costatus": (
                        p["appointed_to"]["company_status"]
                        if "company_status" in p["appointed_to"]
                        else ""
                    ),
                    "coname": (
                        p["appointed_to"]["company_name"]
                        if "company_name" in p["appointed_to"]
                        else ""
                    ),
                }
                for p in ooo["items"]
            ]
            z = []
            for y in x:
                if y["conum"] not in cosdone:
                    z.append(y)
                    cosdone.append(y["conum"])
            if isinstance(z, dict):
                z = [z]
            print("Adding {} companies".format(len(z)))
            c.executemany(
                "INSERT INTO companieslite (conum, costatus,coname)"
                "VALUES (:conum,:costatus,:coname)",
                z,
            )
            for i in x:
                cosdone.append(i["conum"])
            # add company director links
            dirnum = ooo["links"]["self"].strip("/").split("/")[1]
            x = [
                {
                    "conum": p["appointed_to"]["company_number"],
                    "dirnum": dirnum,
                    "typ": "current",
                    "status": "director",
                }
                for p in ooo["items"]
            ]
            c.executemany(
                "INSERT INTO codirs (conum, dirnum,typ,status)"
                "VALUES (:conum,:dirnum,:typ,:status)",
                x,
            )
            print("Adding {} company-directorships".format(len(x)))
            dirsparsed.append(oid)
        c.executemany(
            "INSERT INTO coredirs (dirnum) VALUES (?)", [[d] for d in dirsparsed]
        )
        # self.cosparsed.append(seed)
        c.executemany(
            "INSERT INTO singlecos (conum) VALUES (:conum)", [{"conum": seed}]
        )

    def co_director_trawler(
        self, companyseeds=None, maxdepth=3, seeder = True, oneDirSeed = True, typ="current", role="director"
    ):
        """
        A more general corporate network trawler.

        Having used updateOnCo() to find codirectors of a director,
        we now start to explore out from companies where there are at least
        two common directors.

        We then find all the directors of those companies, and the companies they direct.

        We then repeat to the desired depth.

        """
        c = self.db.cursor()

        companyseeds = [] if not companyseeds else companyseeds

        # typ='current'
        # role='director'
        cosparsed = self.get_cosparsed_in_dblite()
        # relaxed=0
        # The depth is how far into the relationship netwrok we want to go
        depth = 0
        while depth < maxdepth:
            print("---------------\nFilling out level - {}...".format(depth))
            # We can use a set of previously discovered directors as the seeds
            if seeder and depth == 0:
                # Another policy would be dive on all companies associated w/ dirs of seed
                # In which case set the above test to depth==0
                tofetch = [
                    u[0] for u in c.execute(""" SELECT DISTINCT conum from codirs""")
                ]
            else:
                # Find companies where there are at least two common directors
                duals = c.execute(
                    """SELECT cd1.conum as c1,cd2.conum as c2, count(*) FROM codirs AS cd1
                                LEFT JOIN codirs AS cd2 
                                ON cd1.dirnum = cd2.dirnum AND cd1.dirnum
                                WHERE cd1.conum < cd2.conum GROUP BY c1,c2 HAVING COUNT(*)>1
                                """
                )
                tofetch = [x for t in duals for x in t[:2]]
                # The above has some issues. eg only 1 director is required, and secretary IDs are unique to company
                # Maybe need to change logic so if two directors OR company just has one director?
                # if relaxed>0:
                #    print('Being relaxed {} at depth {}...'.format(relaxed,depth))
                #    duals=c.execute('''SELECT cd.conum as c1,cl.coname as cn, count(*) FROM codirs as cd JOIN companieslite as cl
                #                 WHERE cd.conum= cl.conum GROUP BY c1,cn HAVING COUNT(*)=1
                #                ''')
                #    tofetch=tofetch+[x[0] for x in duals]
                #    relaxed=relaxed-1
            if depth == 0 and oneDirSeed:
                # add in companies with a single director first time round
                sco = []
                for u in c.execute(
                    """SELECT DISTINCT cd.conum, cl.coname FROM codirs cd JOIN companieslite cl ON cd.conum=cl.conum"""
                ):
                    # apiNice()
                    o = self.ch_getCompanyOfficers(u[0], typ=typ, role=role)
                    if len(o["items"]) == 1 or u[0] in companyseeds:
                        sco.append({"conum": u[0], "coname": u[1]})
                        tofetch.append(u[0])
                # c.executemany(
                #    "INSERT INTO singlecos (conum,coname) VALUES (:conum,:coname)", sco
                # )
            # TO DO: Another stategy might to to try to find the Finance Director or other names role and seed from them?

            # Get undone companies
            print("To fetch: ", [u for u in tofetch if u not in cosparsed])
            for u in [x for x in tofetch if x not in cosparsed]:
                self.updateOnCo(u, typ=typ, role=role)
                cosparsed.append(u)
                # play nice
                # apiNice()
            depth = depth + 1
            # Parse companies

    def generate_nx_model(self, filename=None):
        c = self.db.cursor()

        G = nx.Graph()

        data = c.execute(
            """SELECT cl.conum as cid, cl.coname as cn, dl.dirnum as did, dl.dirname as dn
        FROM codirs AS cd JOIN companieslite as cl JOIN directorslite as dl ON cd.dirnum = dl.dirnum and cd.conum=cl.conum """
        )
        for d in data:
            G.add_node(d[0], Label=d[1])
            G.add_node(d[2], Label=d[3])
            G.add_edge(d[0], d[2])

        # e.g. out.gexf
        if filename:
            nx.write_gexf(G, filename)

        return G

    def visualise_network(self, G):
        pos = nx.fruchterman_reingold_layout(G)
        labels = [G.nodes[node]["Label"] for node in G.nodes]

        for node, position in pos.items():
            G.nodes[node]["pos"] = position

        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]["pos"]
            x1, y1 = G.nodes[edge[1]]["pos"]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color="#888"),
            hoverinfo="none",
            mode="lines",
        )

        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = G.nodes[node]["pos"]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers",
            hoverinfo="text",
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale="YlGnBu",
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title="Node Connections",
                    xanchor="left",
                    titleside="right",
                ),
                line_width=2,
            ),
        )

        node_adjacencies = []
        node_text = []
        for node, adjacencies in G.adjacency():
            # Get the label for the node (stored in the node attributes)
            label = G.nodes[node]["Label"]  # Use the label or fallback to the node ID

            # Get the number of connections (the number of neighbors)
            num_connections = len(adjacencies)

            # Append the number of connections to node_adjacencies for color mapping
            node_adjacencies.append(num_connections)

            # Create hover text with the node label and number of connections
            node_text.append(f"Label: {label} - # of connections: {num_connections}")

        # Assign the number of connections to the node marker color
        node_trace.marker.color = node_adjacencies

        # Assign the text for hover info
        node_trace.text = node_text

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title="<br>Network graph made with Python",
                titlefont_size=16,
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[
                    dict(
                        text="Corporate network",
                        showarrow=False,
                        xref="paper",
                        yref="paper",
                        x=0.005,
                        y=-0.002,
                    )
                ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            ),
        )

        # fig.show()
        return fig
