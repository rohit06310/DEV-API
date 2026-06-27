PYTHON_TEMPLATES = {
    "GitHub REST API": '''\
"""
DevFlow SDK  ·  GitHub REST API  ·  Python
"""
import requests
from typing import Optional, Dict, Any


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str) -> None:
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    def get_repository(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch repository metadata."""
        resp = self.session.get(f"{self.BASE_URL}/repos/{owner}/{repo}")
        resp.raise_for_status()
        return resp.json()

    def list_commits(
        self,
        owner: str,
        repo: str,
        sha: Optional[str] = None,
        per_page: int = 30,
    ) -> list:
        params: Dict[str, Any] = {"per_page": per_page}
        if sha:
            params["sha"] = sha
        resp = self.session.get(
            f"{self.BASE_URL}/repos/{owner}/{repo}/commits",
            params=params,
        )
        resp.raise_for_status()
        return resp.json()

    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str = "",
        labels: Optional[list] = None,
    ) -> Dict[str, Any]:
        payload = {"title": title, "body": body, "labels": labels or []}
        resp = self.session.post(
            f"{self.BASE_URL}/repos/{owner}/{repo}/issues",
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()

    def search_repositories(self, query: str, sort: str = "stars") -> Dict[str, Any]:
        resp = self.session.get(
            f"{self.BASE_URL}/search/repositories",
            params={"q": query, "sort": sort},
        )
        resp.raise_for_status()
        return resp.json()


# ── Quick start ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    client = GitHubClient(token="YOUR_GITHUB_TOKEN")

    repo = client.get_repository("octocat", "Hello-World")
    print(f"Stars: {repo['stargazers_count']}")

    commits = client.list_commits("octocat", "Hello-World", per_page=5)
    for c in commits:
        print(c["commit"]["message"][:72])
''',
    "Stripe API": '''\
"""
DevFlow SDK  ·  Stripe API  ·  Python
"""
import requests
from requests.auth import HTTPBasicAuth
from typing import Optional, Dict, Any


class StripeClient:
    BASE_URL = "https://api.stripe.com/v1"

    def __init__(self, api_key: str) -> None:
        self.auth = HTTPBasicAuth(api_key, "")
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Stripe-Version": "2024-06-20",
        }

    def create_payment_intent(
        self,
        amount: int,
        currency: str = "usd",
        payment_method_types: Optional[list] = None,
    ) -> Dict[str, Any]:
        data = {
            "amount": amount,
            "currency": currency,
            "payment_method_types[]": (payment_method_types or ["card"])[0],
        }
        resp = requests.post(
            f"{self.BASE_URL}/payment_intents",
            data=data,
            auth=self.auth,
            headers=self.headers,
        )
        resp.raise_for_status()
        return resp.json()

    def create_customer(self, email: str, name: str = "") -> Dict[str, Any]:
        resp = requests.post(
            f"{self.BASE_URL}/customers",
            data={"email": email, "name": name},
            auth=self.auth,
            headers=self.headers,
        )
        resp.raise_for_status()
        return resp.json()

    def list_charges(self, limit: int = 10) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.BASE_URL}/charges",
            params={"limit": limit},
            auth=self.auth,
        )
        resp.raise_for_status()
        return resp.json()


# ── Quick start ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    client = StripeClient(api_key="sk_test_YOUR_KEY")

    pi = client.create_payment_intent(amount=2000, currency="usd")
    print(f"PaymentIntent: {pi['id']}  status={pi['status']}")

    customer = client.create_customer(email="user@example.com", name="Jane Doe")
    print(f"Customer: {customer['id']}")
''',
    "Twilio API": '''\
"""
DevFlow SDK  ·  Twilio API  ·  Python
"""
import requests
from requests.auth import HTTPBasicAuth
from typing import Optional, Dict, Any


class TwilioClient:
    BASE_URL = "https://api.twilio.com/2010-04-01"

    def __init__(self, account_sid: str, auth_token: str) -> None:
        self.account_sid = account_sid
        self.auth = HTTPBasicAuth(account_sid, auth_token)
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def send_sms(self, to: str, from_: str, body: str) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.BASE_URL}/Accounts/{self.account_sid}/Messages.json",
            data={"To": to, "From": from_, "Body": body},
            auth=self.auth,
            headers=self.headers,
        )
        resp.raise_for_status()
        return resp.json()

    def make_call(self, to: str, from_: str, url: str) -> Dict[str, Any]:
        resp = requests.post(
            f"{self.BASE_URL}/Accounts/{self.account_sid}/Calls.json",
            data={"To": to, "From": from_, "Url": url},
            auth=self.auth,
            headers=self.headers,
        )
        resp.raise_for_status()
        return resp.json()

    def list_messages(self, page_size: int = 20) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.BASE_URL}/Accounts/{self.account_sid}/Messages.json",
            params={"PageSize": page_size},
            auth=self.auth,
        )
        resp.raise_for_status()
        return resp.json()


# ── Quick start ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    client = TwilioClient(
        account_sid="ACXXXXXXXXXXXXXXXX",
        auth_token="your_auth_token",
    )

    msg = client.send_sms(to="+15551234567", from_="+15557654321", body="Hello from DevFlow!")
    print(f"SMS SID: {msg['sid']}  status={msg['status']}")
''',
}

JAVASCRIPT_TEMPLATES = {
    "GitHub REST API": '''\
/**
 * DevFlow SDK  ·  GitHub REST API  ·  JavaScript (Node.js / Browser)
 */

class GitHubClient {
  #baseUrl = "https://api.github.com";
  #headers;

  constructor(token) {
    this.#headers = {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
    };
  }

  async #request(path, options = {}) {
    const res = await fetch(`${this.#baseUrl}${path}`, {
      ...options,
      headers: { ...this.#headers, ...options.headers },
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(`GitHub API error ${res.status}: ${err.message ?? res.statusText}`);
    }
    return res.json();
  }

  getRepository(owner, repo) {
    return this.#request(`/repos/${owner}/${repo}`);
  }

  listCommits(owner, repo, { sha, perPage = 30 } = {}) {
    const params = new URLSearchParams({ per_page: perPage });
    if (sha) params.set("sha", sha);
    return this.#request(`/repos/${owner}/${repo}/commits?${params}`);
  }

  createIssue(owner, repo, { title, body = "", labels = [] }) {
    return this.#request(`/repos/${owner}/${repo}/issues`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, body, labels }),
    });
  }

  searchRepositories(query, sort = "stars") {
    const params = new URLSearchParams({ q: query, sort });
    return this.#request(`/search/repositories?${params}`);
  }
}

// ── Quick start ──────────────────────────────────────────────────────────────
const client = new GitHubClient("YOUR_GITHUB_TOKEN");

client.getRepository("octocat", "Hello-World")
  .then(repo => console.log(`Stars: ${repo.stargazers_count}`))
  .catch(console.error);

client.listCommits("octocat", "Hello-World", { perPage: 5 })
  .then(commits => commits.forEach(c => console.log(c.commit.message.slice(0, 72))))
  .catch(console.error);
''',
    "Stripe API": '''\
/**
 * DevFlow SDK  ·  Stripe API  ·  JavaScript (Node.js)
 */

const https = require("https");
const querystring = require("querystring");

class StripeClient {
  #baseUrl = "api.stripe.com";
  #apiKey;
  #apiVersion = "2024-06-20";

  constructor(apiKey) {
    this.#apiKey = apiKey;
  }

  #request(method, path, data = {}) {
    const body = querystring.stringify(data);
    return new Promise((resolve, reject) => {
      const req = https.request(
        {
          hostname: this.#baseUrl,
          path: `/v1${path}`,
          method,
          auth: `${this.#apiKey}:`,
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "Stripe-Version": this.#apiVersion,
            "Content-Length": Buffer.byteLength(body),
          },
        },
        (res) => {
          let raw = "";
          res.on("data", (chunk) => (raw += chunk));
          res.on("end", () => {
            const json = JSON.parse(raw);
            res.statusCode >= 400 ? reject(json.error) : resolve(json);
          });
        }
      );
      req.on("error", reject);
      req.write(body);
      req.end();
    });
  }

  createPaymentIntent(amount, currency = "usd") {
    return this.#request("POST", "/payment_intents", {
      amount,
      currency,
      "payment_method_types[]": "card",
    });
  }

  createCustomer(email, name = "") {
    return this.#request("POST", "/customers", { email, name });
  }

  listCharges(limit = 10) {
    return this.#request("GET", `/charges?limit=${limit}`);
  }
}

// ── Quick start ──────────────────────────────────────────────────────────────
async function main() {
  const client = new StripeClient("sk_test_YOUR_KEY");

  const pi = await client.createPaymentIntent(2000, "usd");
  console.log(`PaymentIntent: ${pi.id}  status=${pi.status}`);

  const customer = await client.createCustomer("user@example.com", "Jane Doe");
  console.log(`Customer: ${customer.id}`);
}

main().catch(console.error);
''',
    "Twilio API": '''\
/**
 * DevFlow SDK  ·  Twilio API  ·  JavaScript (Node.js)
 */

const https = require("https");
const querystring = require("querystring");

class TwilioClient {
  #baseUrl = "api.twilio.com";
  #accountSid;
  #authToken;

  constructor(accountSid, authToken) {
    this.#accountSid = accountSid;
    this.#authToken = authToken;
  }

  #request(method, path, data = {}) {
    const body = querystring.stringify(data);
    const auth = Buffer.from(`${this.#accountSid}:${this.#authToken}`).toString("base64");
    return new Promise((resolve, reject) => {
      const req = https.request(
        {
          hostname: this.#baseUrl,
          path: `/2010-04-01/Accounts/${this.#accountSid}${path}`,
          method,
          headers: {
            Authorization: `Basic ${auth}`,
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": Buffer.byteLength(body),
          },
        },
        (res) => {
          let raw = "";
          res.on("data", (chunk) => (raw += chunk));
          res.on("end", () => resolve(JSON.parse(raw)));
        }
      );
      req.on("error", reject);
      req.write(body);
      req.end();
    });
  }

  sendSMS(to, from_, body) {
    return this.#request("POST", "/Messages.json", { To: to, From: from_, Body: body });
  }

  makeCall(to, from_, url) {
    return this.#request("POST", "/Calls.json", { To: to, From: from_, Url: url });
  }

  listMessages(pageSize = 20) {
    return this.#request("GET", `/Messages.json?PageSize=${pageSize}`);
  }
}

// ── Quick start ──────────────────────────────────────────────────────────────
const client = new TwilioClient("ACXXXXXXXXXXXXXXXX", "your_auth_token");

client.sendSMS("+15551234567", "+15557654321", "Hello from DevFlow!")
  .then(msg => console.log(`SMS SID: ${msg.sid}`))
  .catch(console.error);
''',
}

JAVA_TEMPLATES = {
    "GitHub REST API": '''\
/**
 * DevFlow SDK  ·  GitHub REST API  ·  Java 17+
 */

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpRequest.BodyPublishers;

public class GitHubClient {

    private static final String BASE_URL = "https://api.github.com";
    private final HttpClient http = HttpClient.newHttpClient();
    private final String token;

    public GitHubClient(String token) {
        this.token = token;
    }

    private HttpRequest.Builder builder(String path) {
        return HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + path))
                .header("Authorization", "Bearer " + token)
                .header("Accept", "application/vnd.github+json")
                .header("X-GitHub-Api-Version", "2022-11-28");
    }

    public String getRepository(String owner, String repo) throws Exception {
        var req = builder("/repos/" + owner + "/" + repo).GET().build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }

    public String listCommits(String owner, String repo) throws Exception {
        var req = builder("/repos/" + owner + "/" + repo + "/commits?per_page=30").GET().build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }

    public String createIssue(String owner, String repo, String title, String body) throws Exception {
        String json = String.format(
                """
                {"title":"%s","body":"%s"}
                """, title, body).strip();
        var req = builder("/repos/" + owner + "/" + repo + "/issues")
                .header("Content-Type", "application/json")
                .POST(BodyPublishers.ofString(json))
                .build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }

    // ── Quick start ──────────────────────────────────────────────────────────
    public static void main(String[] args) throws Exception {
        var client = new GitHubClient("YOUR_GITHUB_TOKEN");

        String repoJson = client.getRepository("octocat", "Hello-World");
        System.out.println(repoJson);

        String issue = client.createIssue("octocat", "Hello-World",
                "Bug report", "Steps to reproduce...");
        System.out.println(issue);
    }
}
''',
    "Stripe API": '''\
/**
 * DevFlow SDK  ·  Stripe API  ·  Java 17+
 */

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpRequest.BodyPublishers;
import java.util.Base64;

public class StripeClient {

    private static final String BASE_URL = "https://api.stripe.com/v1";
    private final HttpClient http = HttpClient.newHttpClient();
    private final String encodedKey;

    public StripeClient(String apiKey) {
        this.encodedKey = Base64.getEncoder().encodeToString((apiKey + ":").getBytes());
    }

    private HttpRequest.Builder builder(String path) {
        return HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + path))
                .header("Authorization", "Basic " + encodedKey)
                .header("Stripe-Version", "2024-06-20")
                .header("Content-Type", "application/x-www-form-urlencoded");
    }

    public String createPaymentIntent(long amount, String currency) throws Exception {
        String body = "amount=" + amount + "&currency=" + currency + "&payment_method_types[]=card";
        var req = builder("/payment_intents").POST(BodyPublishers.ofString(body)).build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }

    public String createCustomer(String email, String name) throws Exception {
        String body = "email=" + email + "&name=" + name;
        var req = builder("/customers").POST(BodyPublishers.ofString(body)).build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }

    public String listCharges(int limit) throws Exception {
        var req = builder("/charges?limit=" + limit).GET().build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }

    // ── Quick start ──────────────────────────────────────────────────────────
    public static void main(String[] args) throws Exception {
        var client = new StripeClient("sk_test_YOUR_KEY");

        String pi = client.createPaymentIntent(2000L, "usd");
        System.out.println("PaymentIntent: " + pi);

        String customer = client.createCustomer("user@example.com", "Jane Doe");
        System.out.println("Customer: " + customer);
    }
}
''',
    "Twilio API": '''\
/**
 * DevFlow SDK  ·  Twilio API  ·  Java 17+
 */

import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpRequest.BodyPublishers;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class TwilioClient {

    private static final String BASE_URL = "https://api.twilio.com/2010-04-01";
    private final HttpClient http = HttpClient.newHttpClient();
    private final String accountSid;
    private final String encodedAuth;

    public TwilioClient(String accountSid, String authToken) {
        this.accountSid = accountSid;
        this.encodedAuth = Base64.getEncoder()
                .encodeToString((accountSid + ":" + authToken).getBytes());
    }

    private HttpRequest.Builder builder(String path) {
        return HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/Accounts/" + accountSid + path))
                .header("Authorization", "Basic " + encodedAuth)
                .header("Content-Type", "application/x-www-form-urlencoded");
    }

    private static String encode(String s) {
        return URLEncoder.encode(s, StandardCharsets.UTF_8);
    }

    public String sendSMS(String to, String from, String body) throws Exception {
        String form = "To=" + encode(to) + "&From=" + encode(from) + "&Body=" + encode(body);
        var req = builder("/Messages.json").POST(BodyPublishers.ofString(form)).build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }

    public String makeCall(String to, String from, String url) throws Exception {
        String form = "To=" + encode(to) + "&From=" + encode(from) + "&Url=" + encode(url);
        var req = builder("/Calls.json").POST(BodyPublishers.ofString(form)).build();
        return http.send(req, HttpResponse.BodyHandlers.ofString()).body();
    }

    // ── Quick start ──────────────────────────────────────────────────────────
    public static void main(String[] args) throws Exception {
        var client = new TwilioClient("ACXXXXXXXXXXXXXXXX", "your_auth_token");

        String msg = client.sendSMS("+15551234567", "+15557654321", "Hello from DevFlow!");
        System.out.println("SMS: " + msg);
    }
}
''',
}

EXAMPLES = {
    "GitHub REST API": {
        "quickstart": """\
# Quick Start — GitHub REST API

import requests

TOKEN = "YOUR_GITHUB_TOKEN"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Fetch a repository
resp = requests.get("https://api.github.com/repos/octocat/Hello-World", headers=headers)
repo = resp.json()
print(f"Repo: {repo['full_name']}  ⭐ {repo['stargazers_count']}")
""",
        "auth": """\
# Authentication — GitHub REST API

# 1. Personal Access Token (recommended for scripts)
headers = {"Authorization": "Bearer ghp_your_personal_access_token"}

# 2. OAuth App Token
headers = {"Authorization": "token oauth_access_token"}

# 3. GitHub App JWT (for server-to-server)
import jwt, time
payload = {
    "iat": int(time.time()),
    "exp": int(time.time()) + (10 * 60),
    "iss": "YOUR_APP_ID",
}
jwt_token = jwt.encode(payload, open("private-key.pem").read(), algorithm="RS256")
headers = {"Authorization": f"Bearer {jwt_token}"}
""",
        "endpoint_usage": """\
# Endpoint Usage — Repos, Issues & Search

import requests

client = requests.Session()
client.headers.update({
    "Authorization": "Bearer YOUR_TOKEN",
    "Accept": "application/vnd.github+json",
})

BASE = "https://api.github.com"

# List commits with pagination
commits = client.get(f"{BASE}/repos/torvalds/linux/commits", params={"per_page": 5}).json()
for c in commits:
    sha  = c["sha"][:7]
    msg  = c["commit"]["message"].splitlines()[0][:60]
    print(f"[{sha}] {msg}")

# Create an issue
issue = client.post(f"{BASE}/repos/octocat/Hello-World/issues", json={
    "title": "Bug: Unexpected behaviour in login flow",
    "body": "Steps to reproduce...",
    "labels": ["bug"],
}).json()
print(f"Issue #{issue['number']} created: {issue['html_url']}")

# Search public repositories
results = client.get(f"{BASE}/search/repositories", params={
    "q": "language:python stars:>5000",
    "sort": "stars",
    "per_page": 3,
}).json()
for r in results["items"]:
    print(f"{r['full_name']}  ⭐ {r['stargazers_count']}")
""",
    },
    "Stripe API": {
        "quickstart": """\
# Quick Start — Stripe API

import requests
from requests.auth import HTTPBasicAuth

API_KEY = "sk_test_YOUR_KEY"
auth    = HTTPBasicAuth(API_KEY, "")
headers = {"Stripe-Version": "2024-06-20"}

# Retrieve account balance
resp = requests.get("https://api.stripe.com/v1/balance", auth=auth, headers=headers)
balance = resp.json()
available = balance["available"][0]
print(f"Available: {available['amount'] / 100:.2f} {available['currency'].upper()}")
""",
        "auth": """\
# Authentication — Stripe API

import requests
from requests.auth import HTTPBasicAuth

# Test keys (safe for development)
TEST_KEY = "sk_test_YOUR_KEY"
auth     = HTTPBasicAuth(TEST_KEY, "")          # password is always empty

# Live keys (production only)
LIVE_KEY = "sk_live_YOUR_KEY"
live_auth = HTTPBasicAuth(LIVE_KEY, "")

# Restricted API keys (recommended for production)
RESTRICTED_KEY = "rk_live_YOUR_RESTRICTED_KEY"
restricted_auth = HTTPBasicAuth(RESTRICTED_KEY, "")

# Stripe-Version header ensures stable API behaviour
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Stripe-Version": "2024-06-20",
}
""",
        "endpoint_usage": """\
# Endpoint Usage — Payments, Customers & Subscriptions

import requests
from requests.auth import HTTPBasicAuth

auth    = HTTPBasicAuth("sk_test_YOUR_KEY", "")
BASE    = "https://api.stripe.com/v1"
headers = {"Stripe-Version": "2024-06-20"}

# Create a customer
customer = requests.post(f"{BASE}/customers",
    data={"email": "jane@example.com", "name": "Jane Doe"},
    auth=auth, headers=headers).json()
cid = customer["id"]
print(f"Customer: {cid}")

# Create a PaymentIntent
pi = requests.post(f"{BASE}/payment_intents",
    data={"amount": 4999, "currency": "usd", "customer": cid,
          "payment_method_types[]": "card"},
    auth=auth, headers=headers).json()
print(f"PaymentIntent: {pi['id']}  client_secret={pi['client_secret'][:20]}…")

# Create a subscription
price_id = "price_YOUR_PRICE_ID"
sub = requests.post(f"{BASE}/subscriptions",
    data={"customer": cid, "items[0][price]": price_id},
    auth=auth, headers=headers).json()
print(f"Subscription: {sub['id']}  status={sub['status']}")
""",
    },
    "Twilio API": {
        "quickstart": """\
# Quick Start — Twilio API

import requests
from requests.auth import HTTPBasicAuth

ACCOUNT_SID = "ACXXXXXXXXXXXXXXXX"
AUTH_TOKEN  = "your_auth_token"
auth        = HTTPBasicAuth(ACCOUNT_SID, AUTH_TOKEN)
BASE        = f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}"

# Send an SMS
resp = requests.post(f"{BASE}/Messages.json",
    data={
        "To":   "+15551234567",
        "From": "+15557654321",
        "Body": "Hello from DevFlow!",
    },
    auth=auth)
msg = resp.json()
print(f"Message SID: {msg['sid']}  status={msg['status']}")
""",
        "auth": """\
# Authentication — Twilio API

import requests
from requests.auth import HTTPBasicAuth
import base64

ACCOUNT_SID = "ACXXXXXXXXXXXXXXXX"
AUTH_TOKEN  = "your_auth_token"

# Option 1 — HTTPBasicAuth (recommended)
auth = HTTPBasicAuth(ACCOUNT_SID, AUTH_TOKEN)

# Option 2 — Manual Base64 header
credentials = f"{ACCOUNT_SID}:{AUTH_TOKEN}"
encoded     = base64.b64encode(credentials.encode()).decode()
headers     = {"Authorization": f"Basic {encoded}"}

# API Key Auth (scoped, revocable — recommended for production)
API_KEY    = "SKxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
API_SECRET = "your_api_key_secret"
api_auth   = HTTPBasicAuth(API_KEY, API_SECRET)
""",
        "endpoint_usage": """\
# Endpoint Usage — SMS, Calls & Phone Numbers

import requests
from requests.auth import HTTPBasicAuth

SID  = "ACXXXXXXXXXXXXXXXX"
TOK  = "your_auth_token"
auth = HTTPBasicAuth(SID, TOK)
BASE = f"https://api.twilio.com/2010-04-01/Accounts/{SID}"

# Send SMS
sms = requests.post(f"{BASE}/Messages.json",
    data={"To": "+15551234567", "From": "+15557654321", "Body": "Ping!"},
    auth=auth).json()
print(f"SMS {sms['sid']} → {sms['status']}")

# Retrieve message list
messages = requests.get(f"{BASE}/Messages.json", params={"PageSize": 5}, auth=auth).json()
for m in messages.get("messages", []):
    print(f"[{m['date_sent']}] {m['from_']} → {m['to']}: {m['body'][:40]}")

# Make a voice call
call = requests.post(f"{BASE}/Calls.json",
    data={
        "To":   "+15551234567",
        "From": "+15557654321",
        "Url":  "https://demo.twilio.com/docs/voice.xml",
    },
    auth=auth).json()
print(f"Call SID: {call['sid']}  status={call['status']}")
""",
    },
}
