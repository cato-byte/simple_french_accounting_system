# 🇫🇷 Minimum Legal Requirements for an Accounting App in France

This document outlines the minimum legal requirements your accounting application must meet to comply with French laws and tax regulations. This is particularly relevant for auto-entrepreneurs, SMEs (SARL, SAS), and any business subject to commercial accounting.

---

## 1. 🔒 Inalterability (`Inaltérabilité`)
- Entries must **not be modifiable** after registration.
- Corrections must be made through **new adjusting entries**, not overwriting.
- A **traceable audit log** of changes must be maintained.

---

## 2. 🛡️ Security (`Sécurisation`)
- Data must be protected from unauthorized access.
- Implementation of **user authentication**, **role-based access control**, and **data encryption** is required.

---

## 3. 🗃️ Archiving (`Archivage`)
- Accounting data must be archived in a **durable and unalterable format**.
- Data retention: **10 years** (as per Article L123-22 of the Code de commerce).
- Archived records should include **timestamps** and be resistant to modification.

---

## 4. 🧾 Reliable Audit Trail (`Piste d’audit fiable`)
- Each transaction must be **traceable to its origin** (invoice, receipt, etc.).
- Logs must be **chronological** and maintain **proof of each operation**.
- Supporting documents must be linked and stored.

---

## 5. 💰 VAT Compliance (if applicable)
If the user is subject to VAT:
- Track **collected and deductible VAT**.
- Support **CA3 VAT declarations**.
- Ensure **invoice management**:
  - Sequential numbering
  - Required fields (e.g., SIRET, VAT number)

---

## 6. 🧾 FEC Export (`Fichier des Écritures Comptables`)
- The app must generate a **valid FEC file** on demand during tax audits.
- The FEC format must comply with **DGFiP specifications**.
- Required for companies under the *régime réel* accounting scheme.

---

## 7. ✅ Certified Software for POS (if applicable)
If the app includes **cash register/point-of-sale (POS)** functionalities:
- Certification is mandatory if the user:
  - Handles B2C payments
  - Is subject to VAT
- Certification options:
  - **NF525 Certification (LNE)**
  - **Self-certification (Attestation de conformité)**

---

## 8. 🔢 Numbering & Chronology
- Invoices and entries must be:
  - **Sequentially numbered**
  - **Chronologically ordered**
- No deletion or insertion of entries mid-sequence is allowed.

---

## 🛠️ Optional but Recommended Features
While not legally required, the following are considered best practice:
- Supplier and customer database
- Expense tracking with receipt uploads
- Bank reconciliation tools
- Real-time balance sheet and profit & loss view
- Support for multi-language and multi-currency

---

## 📎 References
- [Article L123-22 - Code de commerce](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006468156/)
- [Fichier des Écritures Comptables - DGFiP](https://www.impots.gouv.fr/fiche-des-ecritures-comptables-fec)
- [NF525 Certification](https://www.lne.fr/fr/certification/nf525-certification-des-logiciels-de-caisse)
- [DGFiP VAT Software Guidelines](https://www.impots.gouv.fr)

---

> 📄 Maintainer Note: Ifr app evolves, make sure to revisit this document and ensure continued compliance with new French regulations.
