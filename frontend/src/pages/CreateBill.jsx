import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Trash, Save, Printer } from 'lucide-react';
import api from '../api/axios';

const CreateBill = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [billId, setBillId] = useState(null);
    const [customer, setCustomer] = useState({
        name: '',
        phone: '',
    });
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);

    const [items, setItems] = useState([
        { item_name: '', price: '', quantity: 1, item_total: 0 }
    ]);
    const [paymentStatus, setPaymentStatus] = useState('Unpaid');
    const [paymentMode, setPaymentMode] = useState('Cash');
    const [discount, setDiscount] = useState(0);
    const [discountType, setDiscountType] = useState('Amount'); // 'Amount' or 'Percentage'

    const handleItemChange = (index, field, value) => {
        const newItems = [...items];
        newItems[index][field] = value;

        if (field === 'price' || field === 'quantity') {
            const price = parseFloat(newItems[index].price) || 0;
            const qty = parseInt(newItems[index].quantity) || 0;
            newItems[index].item_total = price * qty;
        }

        setItems(newItems);
    };

    const addItem = () => {
        setItems([...items, { item_name: '', price: '', quantity: 1, item_total: 0 }]);
    };

    const removeItem = (index) => {
        const newItems = items.filter((_, i) => i !== index);
        setItems(newItems);
    };

    const calculateSubtotal = () => {
        return items.reduce((acc, item) => acc + (parseFloat(item.item_total) || 0), 0);
    };

    const calculateDiscountAmount = () => {
        const subtotal = calculateSubtotal();
        const value = parseFloat(discount) || 0;
        if (discountType === 'Percentage') {
            return (subtotal * value) / 100;
        }
        return value;
    };

    const calculateTotal = () => {
        return calculateSubtotal() - calculateDiscountAmount();
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const payload = {
                customer_name: customer.name,
                customer_phone: customer.phone,
                date: new Date(date).toISOString(),
                total_amount: calculateTotal(),
                items: items.map(item => ({
                    item_name: item.item_name,
                    price: parseFloat(item.price),
                    quantity: parseInt(item.quantity),
                    item_total: parseFloat(item.item_total)
                })),
                items: items.map(item => ({
                    item_name: item.item_name,
                    price: parseFloat(item.price),
                    quantity: parseInt(item.quantity),
                    item_total: parseFloat(item.item_total)
                })),
                discount: calculateDiscountAmount(),
                status: paymentStatus,
                payment_mode: paymentStatus === 'Paid' ? paymentMode : null
            };

            const response = await api.post('/bills/', payload);
            setBillId(response.data.id);
            // alert('Bill saved successfully!');
            // Show success message with WhatsApp hint if paid
            let successMsg = 'Bill created successfully!';
            if (paymentStatus === 'Paid' && customer.phone) {
                successMsg += ' Invoice scheduled for WhatsApp.';
            }
            alert(successMsg);
        } catch (error) {
            console.error('Error saving bill:', error);
            alert('Failed to save bill. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (billId) {
        return (
            <div className="flex flex-col items-center justify-center p-12 bg-white rounded-lg shadow space-y-4">
                <div className="p-4 bg-green-100 rounded-full">
                    <Save className="w-8 h-8 text-green-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900">Bill Saved Successfully!</h2>
                <div className="flex gap-4">
                    <button
                        onClick={() => {
                            setBillId(null);
                            setCustomer({ name: '', phone: '' });
                            setItems([{ item_name: '', price: '', quantity: 1, item_total: 0 }]);
                            setDate(new Date().toISOString().split('T')[0]);
                            setPaymentStatus('Unpaid');
                            setPaymentMode('Cash');
                            setPaymentMode('Cash');
                            setDiscount(0);
                            setDiscountType('Amount');
                        }}
                        className="px-6 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
                    >
                        Create Another
                    </button>
                    <button
                        onClick={() => window.open(`/invoice/${billId}`, '_blank')}
                        className="flex items-center gap-2 px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                    >
                        <Printer className="w-5 h-5" />
                        Print Invoice
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">New Bill Entry</h1>

            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Customer Details Card */}
                <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Customer Name</label>
                            <input
                                type="text"
                                required
                                value={customer.name}
                                onChange={(e) => setCustomer({ ...customer, name: e.target.value })}
                                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                placeholder="Enter name"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                            <input
                                type="tel"
                                required
                                value={customer.phone}
                                onChange={(e) => setCustomer({ ...customer, phone: e.target.value })}
                                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                                placeholder="Enter phone"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                            <input
                                type="date"
                                required
                                value={date}
                                onChange={(e) => setDate(e.target.value)}
                                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                            />
                        </div>
                    </div>
                </div>

                {/* Items Card */}
                <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-lg font-semibold text-gray-900">Items</h2>
                    </div>

                    <div className="space-y-4">
                        <div className="grid grid-cols-12 gap-4 text-sm font-medium text-gray-500 px-2">
                            <div className="col-span-5">Item Name</div>
                            <div className="col-span-2">Price</div>
                            <div className="col-span-2">Quantity</div>
                            <div className="col-span-2">Total</div>
                            <div className="col-span-1"></div>
                        </div>

                        {items.map((item, index) => (
                            <div key={index} className="grid grid-cols-12 gap-4 items-center">
                                <div className="col-span-5">
                                    <input
                                        type="text"
                                        required
                                        value={item.item_name}
                                        onChange={(e) => handleItemChange(index, 'item_name', e.target.value)}
                                        className="w-full px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500"
                                        placeholder="Item name"
                                    />
                                </div>
                                <div className="col-span-2">
                                    <input
                                        type="number"
                                        required
                                        min="0"
                                        value={item.price}
                                        onChange={(e) => handleItemChange(index, 'price', e.target.value)}
                                        className="w-full px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500"
                                        placeholder="0.00"
                                    />
                                </div>
                                <div className="col-span-2">
                                    <input
                                        type="number"
                                        required
                                        min="1"
                                        value={item.quantity}
                                        onChange={(e) => handleItemChange(index, 'quantity', e.target.value)}
                                        className="w-full px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500"
                                    />
                                </div>
                                <div className="col-span-2">
                                    <div className="px-3 py-2 bg-gray-50 rounded-lg text-right font-medium text-gray-900">
                                        ₹{item.item_total.toFixed(2)}
                                    </div>
                                </div>
                                <div className="col-span-1 text-center">
                                    <button
                                        type="button"
                                        onClick={() => removeItem(index)}
                                        disabled={items.length === 1}
                                        className="text-red-500 hover:text-red-700 disabled:opacity-50"
                                    >
                                        <Trash className="w-5 h-5" />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>

                    <button
                        type="button"
                        onClick={addItem}
                        className="mt-6 flex items-center gap-2 text-indigo-600 font-medium hover:text-indigo-800"
                    >
                        <Plus className="w-5 h-5" />
                        Add Item
                    </button>
                </div>

                {/* Bill Summary & Discount Section */}
                <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
                    <h3 className="text-lg font-semibold text-gray-800 mb-4">Bill Summary</h3>

                    <div className="flex flex-col md:flex-row gap-8 justify-between">
                        {/* Discount Controls */}
                        <div className="flex-1 max-w-sm">
                            <label className="block text-sm font-medium text-gray-700 mb-2">Discount</label>
                            <div className="flex gap-2 mb-2">
                                <button
                                    type="button"
                                    onClick={() => setDiscountType('Amount')}
                                    className={`flex-1 py-1 px-3 text-sm rounded border ${discountType === 'Amount' ? 'bg-indigo-50 border-indigo-500 text-indigo-700 font-medium' : 'bg-white border-gray-300'}`}
                                >
                                    Fixed (₹)
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setDiscountType('Percentage')}
                                    className={`flex-1 py-1 px-3 text-sm rounded border ${discountType === 'Percentage' ? 'bg-indigo-50 border-indigo-500 text-indigo-700 font-medium' : 'bg-white border-gray-300'}`}
                                >
                                    Percentage (%)
                                </button>
                            </div>
                            <div className="relative">
                                <input
                                    type="number"
                                    min="0"
                                    value={discount}
                                    onChange={(e) => setDiscount(e.target.value)}
                                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500"
                                    placeholder="Enter value"
                                />
                                <span className="absolute right-3 top-2 text-gray-400">
                                    {discountType === 'Percentage' ? '%' : '₹'}
                                </span>
                            </div>
                            {discountType === 'Percentage' && parseFloat(discount) > 0 && (
                                <p className="text-sm text-gray-500 mt-1">
                                    Discount Amount: <span className="font-medium text-red-500">-₹{calculateDiscountAmount().toFixed(2)}</span>
                                </p>
                            )}
                        </div>

                        {/* Totals Display */}
                        <div className="flex-1 max-w-sm space-y-3">
                            <div className="flex justify-between text-gray-600">
                                <span>Subtotal</span>
                                <span>₹{calculateSubtotal().toFixed(2)}</span>
                            </div>
                            <div className="flex justify-between text-red-500 font-medium">
                                <span>Discount</span>
                                <span>- ₹{calculateDiscountAmount().toFixed(2)}</span>
                            </div>
                            <div className="pt-3 border-t border-gray-200 flex justify-between items-center">
                                <span className="text-lg font-bold text-gray-900">Grand Total</span>
                                <span className="text-2xl font-bold text-indigo-600">₹{calculateTotal().toFixed(2)}</span>
                            </div>
                            <p className="text-sm text-gray-500 text-right mt-1">Total Items: {items.reduce((acc, i) => acc + parseInt(i.quantity || 0), 0)}</p>
                        </div>
                    </div>
                </div>

                {/* Payment & Status Section */}
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-800 mb-4">Payment Details</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                Payment Status
                            </label>
                            <div className="flex gap-2">
                                <button
                                    type="button"
                                    onClick={() => setPaymentStatus('Unpaid')}
                                    className={`flex-1 py-2 px-4 rounded-lg border ${paymentStatus === 'Unpaid'
                                        ? 'bg-red-100 border-red-500 text-red-700 font-medium'
                                        : 'bg-white border-gray-300 text-gray-600'
                                        }`}
                                >
                                    Unpaid
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setPaymentStatus('Paid')}
                                    className={`flex-1 py-2 px-4 rounded-lg border ${paymentStatus === 'Paid'
                                        ? 'bg-green-100 border-green-500 text-green-700 font-medium'
                                        : 'bg-white border-gray-300 text-gray-600'
                                        }`}
                                >
                                    Paid
                                </button>
                            </div>
                        </div>

                        {paymentStatus === 'Paid' && (
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">
                                    Payment Mode
                                </label>
                                <select
                                    value={paymentMode}
                                    onChange={(e) => setPaymentMode(e.target.value)}
                                    className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-amber-500 outline-none"
                                >
                                    <option value="Cash">Cash</option>
                                    <option value="UPI">UPI</option>
                                    <option value="Card">Card</option>
                                    <option value="Credit">Credit/Udhaar</option>
                                </select>
                            </div>
                        )}
                    </div>
                </div>

                <div className="flex justify-end">
                    <button
                        type="submit"
                        disabled={loading}
                        className="flex items-center gap-2 px-8 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 shadow-lg shadow-indigo-200"
                    >
                        {loading ? 'Saving...' : (
                            <>
                                <Save className="w-5 h-5" />
                                Save & Generate Invoice
                            </>
                        )}
                    </button>
                </div>
            </form >
        </div >
    );
};

export default CreateBill;
