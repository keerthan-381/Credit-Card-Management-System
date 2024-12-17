import React, { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import "./App.css";

function TransactionDetails() {
  const { cardNumber } = useParams(); // Get card number from the route params
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const response = await fetch(
          `http://localhost:5000/get-transactions/${cardNumber}`
        );
        const data = await response.json();
        if (data.transactions) {
          setTransactions(data.transactions);
        }
      } catch (error) {
        console.error("Error fetching transactions:", error);
      }
    };

    fetchTransactions();
  }, [cardNumber]);

  return (
    <div className="transaction-details">
      <nav className="navbar">
        <div className="logo">O</div>
        <Link to="/user-details">
          <button className="back-button">Back</button>
        </Link>
      </nav>
      <h3>Transaction Details for Card: {cardNumber}</h3>
      {transactions.length > 0 ? (
        <table className="transaction-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Merchant Name</th>
              <th>Category</th>
              <th>Date</th>
              <th>Amount</th>
              <th>Outstanding</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction, index) => (
              <tr key={index}>
                <td>{index + 1}</td>
                <td>{transaction.merchant_name}</td>
                <td>{transaction.category}</td>
                <td>{transaction.transaction_date}</td>
                <td>₹{parseFloat(transaction.amount || 0).toFixed(2)}</td>{" "}
                {/* Safely handle amount */}
                <td>₹{parseFloat(transaction.outstanding || 0).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No transactions available.</p>
      )}
    </div>
  );
}

export default TransactionDetails;
