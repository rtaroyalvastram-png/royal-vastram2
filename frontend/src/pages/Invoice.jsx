import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/axios';

const Invoice = () => {
    const { id } = useParams();
    const [bill, setBill] = useState(null);

    useEffect(() => {
        const fetchBill = async () => {
            try {
                const response = await api.get(`/bills/${id}`);
                setBill(response.data);
            } catch (error) {
                console.error("Failed to fetch bill", error);
            }
        };
        fetchBill();
    }, [id]);

    const handlePrint = () => {
        window.print();
    };

    if (!bill) return <div className="p-8 text-center">Loading Invoice...</div>;

    return (
        <div className="max-w-3xl mx-auto bg-white p-12 min-h-screen text-gray-900">
            {/* Print Button - Hidden when printing */}
            <div className="fixed top-4 right-4 print:hidden">
                <button
                    onClick={handlePrint}
                    className="bg-gray-800 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded shadow flex items-center gap-2"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M6.72 13.829c-.24.03-.48.062-.72.096m.72-.096a42.415 42.415 0 0 1 10.56 0m-10.56 0L6.34 18m10.94-4.171c.24.03.48.062.72.096m-.72-.096L17.66 18m0 0 .229 2.523a1.125 1.125 0 0 1-1.12 1.227H7.231c-.662 0-1.18-.568-1.12-1.227L6.34 18m11.318 0h1.091A2.25 2.25 0 0 0 21 15.75V9.456c0-1.081-.768-2.015-1.837-2.175a48.055 48.055 0 0 0-1.913-.247M6.34 18H5.25A2.25 2.25 0 0 1 3 15.75V9.456c0-1.081.768-2.015 1.837-2.175a48.041 48.041 0 0 1 1.913-.247m10.5 0a48.536 48.536 0 0 0-10.5 0m10.5 0V3.375c0-.621-.504-1.125-1.125-1.125h-8.25c-.621 0-1.125.504-1.125 1.125v3.659M18 10.5h.008v.008H18V10.5Zm-3 0h.008v.008H15V10.5Z" />
                    </svg>
                    Print Invoice
                </button>
            </div>

            {/* Shop Header */}
            <div className="text-center border-b-2 border-amber-600 pb-8 mb-8 relative">
                <img src="/logo.jpg" alt="Logo" className="absolute left-8 top-0 w-24 h-24 object-contain hidden md:block" onError={(e) => e.target.style.display = 'none'} />
                <h1 className="text-4xl font-bold uppercase tracking-widest text-amber-800" style={{ fontFamily: 'serif' }}>Royal Vastram</h1>
                <p className="text-gray-700 mt-2 font-medium">#58 Mookambika Nilaya, 3rd Main Road, 11th Cross</p>
                <p className="text-gray-700">Ramesh Nagara, Marathahalli, Bangalore - 560037</p>
                <div className="flex justify-center mt-3 text-sm text-gray-600">
                    <p>Ph: +91 96119 61979</p>
                </div>
            </div>

            {/* Invoice Info */}
            <div className="flex justify-between mb-8 bg-amber-50 p-6 rounded-lg border border-amber-100">
                <div>
                    <p className="text-amber-800 text-xs uppercase tracking-wide font-bold mb-1">Billed To</p>
                    <h3 className="font-bold text-xl text-gray-900">{bill.customer_name}</h3>
                    <p className="text-gray-600">{bill.customer_phone}</p>
                </div>
                <div className="text-right">
                    <p className="text-amber-800 text-xs uppercase tracking-wide font-bold mb-1">Invoice Details</p>
                    <h3 className="font-bold text-xl text-gray-900">#{bill.id.toString().padStart(6, '0')}</h3>
                    <p className="text-gray-600">
                        {new Date(bill.date).toLocaleString()}
                    </p>
                </div>
            </div>

            {/* Table */}
            <table className="w-full mb-8 border-collapse">
                <thead>
                    <tr className="bg-gray-800 text-white">
                        <th className="text-left py-3 px-4 uppercase text-xs tracking-wider">Item Name</th>
                        <th className="text-right py-3 px-4 uppercase text-xs tracking-wider">Price</th>
                        <th className="text-right py-3 px-4 uppercase text-xs tracking-wider">Qty</th>
                        <th className="text-right py-3 px-4 uppercase text-xs tracking-wider">Total</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                    {bill.items.map((item, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                            <td className="py-3 px-4">{item.item_name}</td>
                            <td className="text-right py-3 px-4">₹{item.price.toFixed(2)}</td>
                            <td className="text-right py-3 px-4">{item.quantity}</td>
                            <td className="text-right py-3 px-4 font-bold text-gray-800">₹{item.item_total.toFixed(2)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Totals */}
            <div className="flex justify-end pt-4">
                <div className="w-72 bg-gray-800 text-white p-6 rounded-lg shadow-lg">
                    <div className="flex justify-between text-xl font-medium">
                        <span>Grand Total</span>
                        <span className="text-amber-400 font-bold">₹{bill.total_amount.toFixed(2)}</span>
                    </div>
                    {bill.discount > 0 && (
                        <div className="flex justify-between text-sm mt-2 text-gray-300">
                            <span>Discount</span>
                            <span>- ₹{bill.discount.toFixed(2)}</span>
                        </div>
                    )}
                </div>
            </div>

            {/* Footer */}
            <div className="mt-16 text-center text-sm text-gray-500">
                <h4 className="font-bold text-gray-800 mb-2">Terms & Conditions</h4>
                <ul className="text-xs space-y-1">
                    <li>1. Goods once sold will not be taken back or exchanged.</li>
                    <li>2. No return/exchange on discounted items.</li>
                    <li>3. Please check the saree before leaving the shop.</li>
                    <li>4. Minor color or weaving variations are not defects.</li>
                    <li>5. We are not responsible for damage after purchase.</li>
                    <li>6. Disputes subject to Bangalore jurisdiction only</li>
                </ul>
                <p className="mt-4 font-medium text-amber-800">Thank you for shopping with Royal Vastram!</p>
            </div>

            <style>
                {`
                    @media print {
                        @page { margin: 5mm; size: auto; }
                        body { 
                            background: white; 
                            -webkit-print-color-adjust: exact !important;
                            print-color-adjust: exact !important;
                        }
                        .print\\:hidden { display: none !important; }
                        /* Force background colors */
                        .bg-gray-800 { background-color: #1f2937 !important; color: white !important; }
                        .bg-amber-50 { background-color: #fffbeb !important; }
                        .bg-gray-50 { background-color: #f9fafb !important; }
                        /* Remove shadows/borders that might look weird */
                        .shadow-lg { box-shadow: none !important; }
                    }
                `}
            </style>
        </div>
    );
};

export default Invoice;
