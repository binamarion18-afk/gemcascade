import React, { useState, useEffect, useCallback } from 'react';
import { Plus, MapPin, DollarSign, MessageSquare, User } from 'lucide-react';

export default function TaskApp() {
  const [tasks, setTasks] = useState([
    { id: 1, title: 'House Cleaning', description: 'Need my apartment cleaned', budget: 5000, location: 'Kisumu', poster: 'John', bids: 2, status: 'open' },
    { id: 2, title: 'Tutoring Help', description: 'Need help with math homework', budget: 3000, location: 'Kisumu', poster: 'Sarah', bids: 1, status: 'open' }
  ]);
  
  const [showModal, setShowModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDesc, setNewDesc] = useState('');
  const [newBudget, setNewBudget] = useState('');
  const [newLocation, setNewLocation] = useState('');
  const [selectedTask, setSelectedTask] = useState(null);
  const [showBidModal, setShowBidModal] = useState(false);
  const [bidAmount, setBidAmount] = useState('');
  const [earnings, setEarnings] = useState(0);
  const [userName, setUserName] = useState('');
  const [bankDetails, setBankDetails] = useState('');
  const [paypalEmail, setPaypalEmail] = useState('');
  const [showPaymentModal, setShowPaymentModal] = useState(false);

  const COMMISSION_RATE = 0.15;

  const handlePostTask = () => {
    if (!newTitle || !newBudget || !userName) {
      alert('Please fill all fields');
      return;
    }
    
    const newTask = {
      id: tasks.length + 1,
      title: newTitle,
      description: newDesc,
      budget: parseInt(newBudget),
      location: newLocation,
      poster: userName,
      bids: 0,
      status: 'open'
    };
    
    setTasks([newTask, ...tasks]);
    setNewTitle('');
    setNewDesc('');
    setNewBudget('');
    setNewLocation('');
    setShowModal(false);
  };

  const handleBid = () => {
    if (!bidAmount) {
      alert('Enter a bid amount');
      return;
    }
    
    const bid = parseInt(bidAmount);
    const commission = Math.round(bid * COMMISSION_RATE);
    
    setEarnings(earnings + commission);
    
    const updatedTasks = tasks.map(t => 
      t.id === selectedTask.id 
        ? { ...t, bids: t.bids + 1, status: 'bidding' }
        : t
    );
    setTasks(updatedTasks);
    
    setBidAmount('');
    setShowBidModal(false);
    alert(`Bid placed! You earned KES ${commission} commission (15% of KES ${bid})`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">TaskGig Kenya</h1>
              <p className="text-gray-600">Earn 15% commission on every task</p>
            </div>
            <div className="text-right">
              <p className="text-sm text-gray-600">Your Earnings</p>
              <p className="text-3xl font-bold text-green-600">KES {earnings.toLocaleString()}</p>
            </div>
          </div>
          
          <div className="mb-4 space-y-3">
            <input 
              type="text" 
              placeholder="Enter your name" 
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="bg-blue-50 p-3 rounded-lg">
              {bankDetails || paypalEmail ? (
                <div>
                  <p className="text-sm text-gray-700 font-semibold">Payment Method:</p>
                  {bankDetails && <p className="text-sm text-gray-600">ATM: {bankDetails}</p>}
                  {paypalEmail && <p className="text-sm text-gray-600">PayPal: {paypalEmail}</p>}
                  <button 
                    onClick={() => setShowPaymentModal(true)}
                    className="text-xs text-blue-600 hover:text-blue-800 mt-2 underline"
                  >
                    Change payment details
                  </button>
                </div>
              ) : (
                <p className="text-sm text-gray-600">No payment method added yet</p>
              )}
            </div>
          </div>
          
          <div className="flex gap-2 mb-4">
            <button 
              onClick={() => setShowModal(true)}
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg flex items-center justify-center gap-2 transition"
            >
              <Plus size={20} /> Post Task
            </button>
            <button 
              onClick={() => setShowPaymentModal(true)}
              className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-lg transition"
            >
              Add Payment
            </button>
          </div>
        </div>

        {/* Tasks Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tasks.map(task => (
            <div key={task.id} className="bg-white rounded-lg shadow-md p-5 hover:shadow-lg transition">
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-bold text-lg text-gray-800">{task.title}</h3>
                <span className={`text-xs font-semibold px-2 py-1 rounded ${task.status === 'open' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                  {task.status.toUpperCase()}
                </span>
              </div>
              
              <p className="text-gray-600 text-sm mb-4">{task.description}</p>
              
              <div className="space-y-2 mb-4 text-sm">
                <div className="flex items-center gap-2 text-gray-700">
                  <DollarSign size={16} className="text-green-600" />
                  <span>Budget: KES {task.budget.toLocaleString()}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-700">
                  <MapPin size={16} className="text-red-600" />
                  <span>{task.location}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-700">
                  <User size={16} className="text-blue-600" />
                  <span>Posted by {task.poster}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-700">
                  <MessageSquare size={16} className="text-purple-600" />
                  <span>{task.bids} bids</span>
                </div>
              </div>
              
              <button 
                onClick={() => {
                  setSelectedTask(task);
                  setShowBidModal(true);
                }}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 rounded-lg transition"
              >
                Place Bid
              </button>
            </div>
          ))}
        </div>

        {tasks.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">No tasks posted yet. Start by creating one!</p>
          </div>
        )}
      </div>

      {/* Post Task Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Post a Task</h2>
            <div className="space-y-4">
              <input 
                type="text" 
                placeholder="Task title" 
                value={newTitle}
                onChange={(e) => setNewTitle(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <textarea 
                placeholder="Task description" 
                value={newDesc}
                onChange={(e) => setNewDesc(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 h-24"
              />
              <input 
                type="number" 
                placeholder="Budget (KES)" 
                value={newBudget}
                onChange={(e) => setNewBudget(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input 
                type="text" 
                placeholder="Location" 
                value={newLocation}
                onChange={(e) => setNewLocation(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <div className="flex gap-3">
                <button 
                  onClick={() => setShowModal(false)}
                  className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 rounded-lg transition"
                >
                  Cancel
                </button>
                <button 
                  onClick={handlePostTask}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg transition"
                >
                  Post Task
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Bid Modal */}
      {showBidModal && selectedTask && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-2">{selectedTask.title}</h2>
            <p className="text-gray-600 mb-4">Budget: KES {selectedTask.budget.toLocaleString()}</p>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold mb-2">Your Bid Amount (KES)</label>
                <input 
                  type="number" 
                  placeholder="Enter bid amount" 
                  value={bidAmount}
                  onChange={(e) => setBidAmount(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                {bidAmount && (
                  <p className="text-sm text-green-600 mt-2">
                    Your commission (15%): KES {Math.round(parseInt(bidAmount) * 0.15).toLocaleString()}
                  </p>
                )}
              </div>
              <div className="flex gap-3">
                <button 
                  onClick={() => setShowBidModal(false)}
                  className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 rounded-lg transition"
                >
                  Cancel
                </button>
                <button 
                  onClick={handleBid}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-lg transition"
                >
                  Place Bid
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Payment Details Modal */}
      {showPaymentModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Add Payment Method</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-semibold mb-2">ATM/Bank Card Number</label>
                <input 
                  type="text" 
                  placeholder="e.g., 1234 5678 9012 3456" 
                  value={bankDetails}
                  onChange={(e) => setBankDetails(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <p className="text-xs text-gray-500 mt-1">Your earnings will be sent to this card</p>
              </div>
              <div className="border-t pt-4">
                <label className="block text-sm font-semibold mb-2">Or PayPal Email</label>
                <input 
                  type="email" 
                  placeholder="your.email@paypal.com" 
                  value={paypalEmail}
                  onChange={(e) => setPaypalEmail(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                <p className="text-xs text-gray-500 mt-1">Payouts will go to this PayPal account</p>
              </div>
              <p className="text-xs text-gray-600 bg-yellow-50 p-2 rounded">Note: Payouts are sent weekly when you reach KES 500+</p>
              <div className="flex gap-3">
                <button 
                  onClick={() => setShowPaymentModal(false)}
                  className="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 font-semibold py-2 rounded-lg transition"
                >
                  Cancel
                </button>
                <button 
                  onClick={() => {
                    if (bankDetails || paypalEmail) {
                      setShowPaymentModal(false);
                      alert('Payment method saved!');
                    } else {
                      alert('Please add at least one payment method');
                    }
                  }}
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white font-semibold py-2 rounded-lg transition"
                >
                  Save
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
