<script src="webfont.js"></script>
<script src="snap.svg-min.js"></script>
<script src="underscore-min.js"></script>
<script src="sequence-diagram-min.js"></script>

## Functional Dependencies

### 1. Original

1. User

```sequence
ssn -> user_name, password, fname, minit, Lname, bdate, address, email
```

```flow
st=>start: Start
op=>operation: Your Operation
cond=>condition: Yes or No?
e=>end

st->op->cond
cond(yes)->e
cond(no)->op
```

2. User_phone

ssn -> phone

3. Owner

owner_num -> ssn, buyer_num, offer_num

4. Agent

agent_num -> ssn, total_commision, commision_date

5. Buyer

buyer_num -> ssn

6. Property

property_id -> status, price, asking_price......

7. Open_House

agent_num, oh_num -> start_date, end_date, property_id

8. Offer

buyer_num, offer_num -> price, status,offer_date, property_id, agent_num

9. OH_visit

buyer_num -> agent_num, oh_num

### 2. 1NF

### 3. 2NF

### 4. 3NF

## Schema

### 1. Original
![schema](/ERD/schemadiagram.svg)

### 2. 3NF