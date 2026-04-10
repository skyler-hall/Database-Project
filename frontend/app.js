/* =============================================
   THREAD — Clothing Store
   Shared JavaScript
   COP 4710 Final Project
   ============================================= */

/* -----------------------------------------------
   PLACEHOLDER DATA
   (fetch() calls below connect to Flask backend)
   ----------------------------------------------- */

const PRODUCTS = [
  {
    product_id: 1, name: "Classic Oxford Shirt", category: "Tops", base_price: 58.00,
    variants: [
      { id: 101, size: "S",  color: "White", stock: 12 },
      { id: 102, size: "M",  color: "White", stock: 8  },
      { id: 103, size: "L",  color: "Blue",  stock: 3  },
      { id: 104, size: "XL", color: "Blue",  stock: 0  },
    ]
  },
  {
    product_id: 2, name: "Slim Chino Pants", category: "Bottoms", base_price: 72.00,
    variants: [
      { id: 105, size: "30x30", color: "Khaki", stock: 15 },
      { id: 106, size: "32x32", color: "Khaki", stock: 7  },
      { id: 107, size: "34x32", color: "Olive", stock: 2  },
    ]
  },
  {
    product_id: 3, name: "Wool Blend Overcoat", category: "Outerwear", base_price: 195.00,
    variants: [
      { id: 108, size: "S", color: "Camel",    stock: 4 },
      { id: 109, size: "M", color: "Camel",    stock: 6 },
      { id: 110, size: "L", color: "Charcoal", stock: 1 },
    ]
  },
  {
    product_id: 4, name: "Ribbed Knit Sweater", category: "Tops", base_price: 89.00,
    variants: [
      { id: 111, size: "XS", color: "Cream",        stock: 9  },
      { id: 112, size: "S",  color: "Cream",        stock: 11 },
      { id: 113, size: "M",  color: "Forest Green", stock: 5  },
    ]
  },
  {
    product_id: 5, name: "Canvas Tote Bag", category: "Accessories", base_price: 34.00,
    variants: [
      { id: 114, size: "One Size", color: "Natural", stock: 20 },
      { id: 115, size: "One Size", color: "Black",   stock: 14 },
    ]
  },
  {
    product_id: 6, name: "High-Waist Denim", category: "Bottoms", base_price: 95.00,
    variants: [
      { id: 116, size: "26", color: "Light Wash", stock: 0 },
      { id: 117, size: "28", color: "Dark Wash",  stock: 6 },
      { id: 118, size: "30", color: "Dark Wash",  stock: 3 },
    ]
  },
];

let CUSTOMERS = [
  { email: "jsmith@email.com",  firstName: "Jane",  lastName: "Smith",  address: "123 Oak Ave, Miami, FL",     member: true  },
  { email: "mlopez@email.com",  firstName: "Marco", lastName: "Lopez",  address: "456 Coral Way, Orlando, FL", member: false },
  { email: "alee@email.com",    firstName: "Amy",   lastName: "Lee",    address: "789 Palm Dr, Tampa, FL",     member: true  },
  { email: "tchen@email.com",   firstName: "Tyler", lastName: "Chen",   address: "321 Bay Blvd, Naples, FL",   member: false },
];

const ORDERS = [
  {
    order_id: 1001, customer_email: "jsmith@email.com",
    order_date: "2025-03-01", status: "delivered",
    shipping_address: "123 Oak Ave, Miami, FL", total_amount: 164.00,
    items: [
      { product_id: 1, product_name: "Classic Oxford Shirt", quantity: 1, unit_price: 58.00 },
      { product_id: 2, product_name: "Slim Chino Pants",     quantity: 1, unit_price: 72.00 },
      { product_id: 5, product_name: "Canvas Tote Bag",      quantity: 1, unit_price: 34.00 },
    ]
  },
  {
    order_id: 1002, customer_email: "mlopez@email.com",
    order_date: "2025-03-03", status: "shipped",
    shipping_address: "456 Coral Way, Orlando, FL", total_amount: 195.00,
    items: [
      { product_id: 3, product_name: "Wool Blend Overcoat", quantity: 1, unit_price: 195.00 },
    ]
  },
  {
    order_id: 1003, customer_email: "alee@email.com",
    order_date: "2025-03-04", status: "pending",
    shipping_address: "789 Palm Dr, Tampa, FL", total_amount: 178.00,
    items: [
      { product_id: 4, product_name: "Ribbed Knit Sweater", quantity: 2, unit_price: 89.00 },
    ]
  },
  {
    order_id: 1004, customer_email: "tchen@email.com",
    order_date: "2025-03-05", status: "pending",
    shipping_address: "321 Bay Blvd, Naples, FL", total_amount: 187.00,
    items: [
      { product_id: 6, product_name: "High-Waist Denim",     quantity: 1, unit_price: 95.00 },
      { product_id: 5, product_name: "Canvas Tote Bag",      quantity: 1, unit_price: 34.00 },
      { product_id: 1, product_name: "Classic Oxford Shirt", quantity: 1, unit_price: 58.00 },
    ]
  },
  {
    order_id: 1005, customer_email: "jsmith@email.com",
    order_date: "2025-03-06", status: "delivered",
    shipping_address: "123 Oak Ave, Miami, FL", total_amount: 161.00,
    items: [
      { product_id: 2, product_name: "Slim Chino Pants",    quantity: 1, unit_price: 72.00 },
      { product_id: 4, product_name: "Ribbed Knit Sweater", quantity: 1, unit_price: 89.00 },
    ]
  },
];


/* -----------------------------------------------
   SHARED HELPERS
   ----------------------------------------------- */

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function getStockStatus(variants) {
  const total = variants.reduce((sum, v) => sum + v.stock, 0);
  if (total === 0) return { label: 'Out of Stock', cls: 'out-stock' };
  if (total <= 5)  return { label: 'Low Stock',    cls: 'low-stock' };
  return               { label: 'In Stock',      cls: 'in-stock'  };
}


/* -----------------------------------------------
   PRODUCTS PAGE
   ----------------------------------------------- */

function renderProductCards(data) {
  const grid = document.getElementById('products-grid');
  if (!grid) return;

  document.getElementById('product-count').textContent = `Showing ${data.length} items`;

  if (data.length === 0) {
    grid.innerHTML = '<div style="padding:80px;text-align:center;color:#6B6560;grid-column:1/-1;">No products found.</div>';
    return;
  }

  grid.innerHTML = data.map(p => {
    const stock    = getStockStatus(p.variants);
    const sizeTags = [...new Set(p.variants.map(v => v.size))]
                       .map(s => `<span class="variant-tag">${s}</span>`).join('');
    return `
      <div class="product-card" data-category="${p.category.toLowerCase()}">
        <div class="product-category">${p.category}</div>
        <div class="product-name">${p.name}</div>
        <div class="product-id">Product ID: ${p.product_id}</div>
        <div class="product-variants">${sizeTags}</div>
        <div class="product-footer">
          <div class="product-price">$${p.base_price.toFixed(2)}</div>
          <span class="stock-badge ${stock.cls}">${stock.label}</span>
        </div>
      </div>`;
  }).join('');
}

function renderVariantsTable(data) {
  const tbody = document.getElementById('variants-body');
  if (!tbody) return;

  tbody.innerHTML = data.flatMap(p =>
    p.variants.map(v => `
      <tr>
        <td>${v.id}</td>
        <td>${p.product_id}</td>
        <td>${p.name}</td>
        <td>${v.size}</td>
        <td>${v.color}</td>
        <td>${v.stock}</td>
        <td>$${p.base_price.toFixed(2)}</td>
      </tr>`)
  ).join('');
}

function filterProducts(category, btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const filtered = category === 'all'
    ? PRODUCTS
    : PRODUCTS.filter(p => p.category.toLowerCase() === category);
  renderProductCards(filtered);
  renderVariantsTable(filtered);
}

function searchProducts(query) {
  const q = query.toLowerCase();
  const result = PRODUCTS.filter(p =>
    p.name.toLowerCase().includes(q) || p.category.toLowerCase().includes(q)
  );
  renderProductCards(result);
  renderVariantsTable(result);
}

if (document.getElementById('products-grid')) {
  renderProductCards(PRODUCTS);
  renderVariantsTable(PRODUCTS);
}


/* -----------------------------------------------
   CUSTOMERS PAGE
   ----------------------------------------------- */

function renderCustomersTable(data) {
  const tbody = document.getElementById('customers-body');
  if (!tbody) return;

  const count = document.getElementById('customer-count');
  if (count) count.textContent = `${data.length} registered customer${data.length !== 1 ? 's' : ''}`;

  tbody.innerHTML = data.map(c => `
    <tr>
      <td>${c.email}</td>
      <td>${c.firstName}</td>
      <td>${c.lastName}</td>
      <td>${c.address || '-'}</td>
      <td><span class="member-badge ${c.member ? 'member-yes' : 'member-no'}">${c.member ? 'Member' : 'Guest'}</span></td>
    </tr>`).join('');
}

function searchCustomers(query) {
  const q = query.toLowerCase();
  renderCustomersTable(CUSTOMERS.filter(c =>
    c.firstName.toLowerCase().includes(q) ||
    c.lastName.toLowerCase().includes(q)  ||
    c.email.toLowerCase().includes(q)
  ));
}

function validateField(id, isValid, message) {
  const input = document.getElementById(id);
  const error = document.getElementById(id + '-error');
  input.classList.remove('error-field');
  error.classList.remove('visible');
  if (!isValid) {
    if (message) error.textContent = message;
    input.classList.add('error-field');
    error.classList.add('visible');
  }
  return isValid;
}

const customerForm = document.getElementById('add-customer-form');
if (customerForm) {
  customerForm.addEventListener('submit', function(e) {
    e.preventDefault();

    const firstName  = document.getElementById('firstName').value.trim();
    const lastName   = document.getElementById('lastName').value.trim();
    const email      = document.getElementById('email').value.trim();
    const address    = document.getElementById('address').value.trim();
    const member     = document.getElementById('member').checked;
    const toast      = document.getElementById('toast');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const valid =
      validateField('firstName', !!firstName) &
      validateField('lastName',  !!lastName) &
      validateField('email', emailRegex.test(email), 'A valid email address is required.');

    if (!valid) {
      toast.className = 'toast error-toast';
      toast.textContent = 'Please fix the errors above before submitting.';
      return;
    }

    if (CUSTOMERS.find(c => c.email === email)) {
      validateField('email', false, 'This email is already registered.');
      toast.className = 'toast error-toast';
      toast.textContent = 'A customer with this email already exists.';
      return;
    }

    /* Live backend call — POST /customers */
    fetch('http://localhost:5000/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        first_name: firstName,
        last_name:  lastName,
        email:      email,
        address:    address || null,
        member:     member
      })
    })
    .then(r => r.json())
    .then(data => {
      if (data.error) {
        toast.className = 'toast error-toast';
        toast.textContent = data.error;
        return;
      }
      CUSTOMERS.push({ email, firstName, lastName, address, member });
      renderCustomersTable(CUSTOMERS);
      customerForm.reset();
      toast.className = 'toast success';
      toast.textContent = `${firstName} ${lastName} has been added successfully.`;
    })
    .catch(() => {
      /* Fallback to local if backend not running */
      CUSTOMERS.push({ email, firstName, lastName, address, member });
      renderCustomersTable(CUSTOMERS);
      customerForm.reset();
      toast.className = 'toast success';
      toast.textContent = `${firstName} ${lastName} added (offline mode).`;
    });
  });
}

if (document.getElementById('customers-body')) {
  /* Try live backend first, fall back to placeholder */
  fetch('http://localhost:5000/customers')
    .then(r => r.json())
    .then(data => {
      CUSTOMERS = data.map(c => ({
        email:     c.email,
        firstName: c.first_name,
        lastName:  c.last_name,
        address:   c.address,
        member:    c.membership === 'Member'
      }));
      renderCustomersTable(CUSTOMERS);
    })
    .catch(() => renderCustomersTable(CUSTOMERS));
}


/* -----------------------------------------------
   ORDERS PAGE
   ----------------------------------------------- */

function renderOrdersTable(data) {
  const tbody = document.getElementById('orders-body');
  if (!tbody) return;

  tbody.innerHTML = data.map(o => `
    <tr onclick="openDrawer(${o.order_id})">
      <td>#${o.order_id}</td>
      <td>${o.customer_email || o.email || ''}</td>
      <td>${o.order_date}</td>
      <td><span class="status-badge status-${o.status}">${capitalize(o.status)}</span></td>
      <td>${o.shipping_address || '-'}</td>
      <td>$${parseFloat(o.total_amount).toFixed(2)}</td>
    </tr>`).join('');
}

function filterOrders(status, btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderOrdersTable(status === 'all' ? ORDERS : ORDERS.filter(o => o.status === status));
}

function openDrawer(id) {
  const order = ORDERS.find(o => o.order_id === id);
  if (!order) return;

  document.getElementById('drawer-content').innerHTML = `
    <div class="drawer-title">Order #${order.order_id}</div>
    <div class="drawer-subtitle">
      ${order.order_date} &nbsp;&middot;&nbsp;
      <span class="status-badge status-${order.status}">${capitalize(order.status)}</span>
    </div>
    <div class="detail-row"><span class="detail-label">Customer</span><span>${order.customer_email || order.email || ''}</span></div>
    <div class="detail-row"><span class="detail-label">Shipping Address</span><span>${order.shipping_address || '-'}</span></div>
    <div class="detail-row">
      <span class="detail-label">Total Amount</span>
      <span style="font-family:'Cormorant Garamond',serif;font-size:20px;">$${parseFloat(order.total_amount).toFixed(2)}</span>
    </div>
    <div class="items-title">Order Items</div>
    ${(order.items || []).map(item => `
      <div class="order-item-row">
        <div>
          <div class="item-name">${item.product_name}</div>
          <div class="item-meta">Product ID: ${item.product_id} &nbsp;&middot;&nbsp; Qty: ${item.quantity}</div>
        </div>
        <div class="item-price">$${(item.unit_price * item.quantity).toFixed(2)}</div>
      </div>`).join('')}
  `;

  document.getElementById('drawer-overlay').classList.add('open');
  document.getElementById('drawer').classList.add('open');
}

function closeDrawer() {
  document.getElementById('drawer-overlay').classList.remove('open');
  document.getElementById('drawer').classList.remove('open');
}

if (document.getElementById('orders-body')) {
  fetch('http://localhost:5000/orders')
    .then(r => r.json())
    .then(data => renderOrdersTable(data))
    .catch(() => renderOrdersTable(ORDERS));
}
