async function addTransaction() {
  const dateInput = document.getElementById("date").value;
  const data = {
      date: dateInput ? dateInput : null, // Use null for current date
      amount: document.getElementById("amount").value,
      category: document.getElementById("category").value,
      description: document.getElementById("description").value,
  };
  const response = await fetch("/add_transaction", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
  });
  const result = await response.json();
  alert(result.message);
}

async function viewTransactions() {
  const data = {
      start_date: document.getElementById("start_date").value,
      end_date: document.getElementById("end_date").value,
  };

  // This logic is now handled by the form POST request.
}
