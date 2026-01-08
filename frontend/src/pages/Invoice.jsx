import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/axios';

const numberToIndianWords = (num) => {
    const a = [
        '', 'One ', 'Two ', 'Three ', 'Four ', 'Five ', 'Six ', 'Seven ', 'Eight ', 'Nine ', 'Ten ',
        'Eleven ', 'Twelve ', 'Thirteen ', 'Fourteen ', 'Fifteen ', 'Sixteen ', 'Seventeen ', 'Eighteen ', 'Nineteen '
    ];
    const b = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];

    const inWords = (n) => {
        if ((n = n.toString()).length > 9) return 'overflow';
        let n_array = ('000000000' + n).slice(-9).match(/^(\d{2})(\d{2})(\d{2})(\d{1})(\d{2})$/);
        if (!n_array) return;
        let str = '';
        str += (n_array[1] != 0) ? (a[Number(n_array[1])] || b[n_array[1][0]] + ' ' + a[n_array[1][1]]) + 'Crore ' : '';
        str += (n_array[2] != 0) ? (a[Number(n_array[2])] || b[n_array[2][0]] + ' ' + a[n_array[2][1]]) + 'Lakh ' : '';
        str += (n_array[3] != 0) ? (a[Number(n_array[3])] || b[n_array[3][0]] + ' ' + a[n_array[3][1]]) + 'Thousand ' : '';
        str += (n_array[4] != 0) ? (a[Number(n_array[4])] || b[n_array[4][0]] + ' ' + a[n_array[4][1]]) + 'Hundred ' : '';
        str += (n_array[5] != 0) ? ((str != '') ? 'and ' : '') + (a[Number(n_array[5])] || b[n_array[5][0]] + ' ' + a[n_array[5][1]]) : '';
        return str;
    };
    return inWords(num);
};

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
            {/* Shop Header */}
            <div className="flex justify-between items-start border-b-2 border-amber-600 pb-8 mb-8">
                {/* Left: Logo */}
                <div className="w-32 flex-shrink-0">
                    <img src="/logo.jpg" alt="Logo" className="w-full h-auto object-contain hidden md:block print:block" onError={(e) => e.target.style.display = 'none'} />
                </div>

                {/* Center: Detail */}
                <div className="flex-1 text-center px-4">
                    <h1 className="text-4xl font-bold uppercase tracking-widest text-amber-800 whitespace-nowrap" style={{ fontFamily: 'serif' }}>Royal Vastram</h1>
                    <p className="text-gray-700 mt-2 font-medium">#58 Mookambika Nilaya, 3rd Main Road, 11th Cross</p>
                    <p className="text-gray-700">Ramesh Nagara, Marathahalli, Bangalore - 560037</p>
                    <div className="flex justify-center mt-3 text-sm text-gray-600">
                        <p>Ph: +91 9110611979</p>
                    </div>
                </div>

                {/* Right: Spacer to keep text centered */}
                <div className="w-32 flex-shrink-0 hidden md:block print:block"></div>
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
                        {bill.items.some(i => i.discount > 0) && (
                            <th className="text-right py-3 px-4 uppercase text-xs tracking-wider">Disc</th>
                        )}
                        <th className="text-right py-3 px-4 uppercase text-xs tracking-wider">Total</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                    {bill.items.map((item, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                            <td className="py-3 px-4">{item.item_name}</td>
                            <td className="text-right py-3 px-4">₹{item.price.toFixed(2)}</td>
                            <td className="text-right py-3 px-4">{item.quantity}</td>
                            {bill.items.some(i => i.discount > 0) && (
                                <td className="text-right py-3 px-4 text-red-600">-₹{item.discount ? item.discount.toFixed(2) : '0.00'}</td>
                            )}
                            <td className="text-right py-3 px-4 font-bold text-gray-800">₹{item.item_total.toFixed(2)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Totals */}
            <div className="flex flex-col items-end pt-4">
                <div className="w-72 bg-white text-gray-900 border border-gray-300 p-6 rounded-lg">
                    {(() => {
                        const grossSubtotal = bill.items.reduce((acc, item) => acc + (item.price * item.quantity), 0);
                        const totalDiscount = grossSubtotal - bill.total_amount;

                        return (
                            <>
                                <div className="flex justify-between text-gray-600 mb-2">
                                    <span>Subtotal</span>
                                    <span>₹{grossSubtotal.toFixed(2)}</span>
                                </div>
                                {totalDiscount > 0.01 && (
                                    <div className="flex justify-between text-red-500 mb-2">
                                        <span>Discount</span>
                                        <span>- ₹{totalDiscount.toFixed(2)}</span>
                                    </div>
                                )}
                                <div className="flex justify-between text-xl font-bold border-t pt-2 mt-2">
                                    <span>Grand Total</span>
                                    <span>₹{bill.total_amount.toFixed(2)}</span>
                                </div>
                            </>
                        );
                    })()}
                </div>
                {/* Amount in Words - Now below the total box */}
                <div className="w-72 mt-2 text-right">
                    <p className="text-sm font-medium text-gray-600 italic">
                        Amount in Words:<br />
                        <span className="text-gray-900 not-italic">{numberToIndianWords(Math.round(bill.total_amount))} Only</span>
                    </p>
                </div>
            </div>

            {/* Footer */}
            <div className="mt-16 text-left text-sm text-gray-500">
                <h4 className="font-bold text-gray-800 mb-2 text-xs uppercase">Terms & Conditions</h4>
                <ul className="text-xs space-y-1 text-left list-disc pl-4">
                    <li>Goods once sold will not be taken back or exchanged.</li>
                    <li>No return/exchange on discounted items.</li>
                    <li>Please check the saree before leaving the shop.</li>
                    <li>Minor color or weaving variations are not defects.</li>
                    <li>We are not responsible for damage after purchase.</li>
                    <li>Disputes subject to Bangalore jurisdiction only</li>
                </ul>
                <p className="mt-8 font-serif text-center text-amber-800 italic text-lg">
                    "Thanks for shopping with us. We hope this saree adds beauty to your special moments"
                </p>
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
