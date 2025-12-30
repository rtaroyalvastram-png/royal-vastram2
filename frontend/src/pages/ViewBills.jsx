import React, { useEffect, useState } from 'react';
import { Download, Search, CheckCircle, XCircle, Calendar } from 'lucide-react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

const ViewBills = () => {
    const navigate = useNavigate();
    const [bills, setBills] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    // Filter States
    const [filterType, setFilterType] = useState('all'); // all, weekly, monthly, custom
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    useEffect(() => {
        fetchBills();
    }, [filterType, startDate, endDate]);

    const getFilterParams = () => {
        const params = {};

        let start = startDate;
        let end = endDate;
        const today = new Date();

        if (filterType === 'weekly') {
            const lastWeek = new Date(today);
            lastWeek.setDate(today.getDate() - 7);
            start = lastWeek.toISOString().split('T')[0];
            end = today.toISOString().split('T')[0];
        } else if (filterType === 'monthly') {
            const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
            const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
            start = firstDay.toISOString().split('T')[0];
            end = lastDay.toISOString().split('T')[0];
        }

        if (start) params.start_date = start;
        if (end) params.end_date = end;

        return params;
    };

    const fetchBills = async () => {
        setLoading(true);
        try {
            const params = getFilterParams();
            // Use the filter endpoint which returns all matching records (or switch to main if needed)
            // Ideally we use /bills/filter for explicit filtering
            const response = await api.get('/bills/filter', { params });
            setBills(response.data);
        } catch (error) {
            console.error('Failed to fetch bills', error);
        } finally {
            setLoading(false);
        }
    };

    const handleExport = async () => {
        try {
            const params = getFilterParams();
            const response = await api.get('/bills/export', {
                params,
                responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'bills_export.csv');
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error) {
            console.error('Export failed', error);
        }
    };

    const filteredBills = bills.filter(bill => {
        const term = searchTerm.toLowerCase();
        return bill.customer_name.toLowerCase().includes(term) ||
            bill.customer_phone.includes(term) ||
            String(bill.id).includes(term);
    });

    const handleFilterTypeChange = (e) => {
        const type = e.target.value;
        setFilterType(type);
        if (type !== 'custom') {
            setStartDate('');
            setEndDate('');
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <h1 className="text-2xl font-bold text-gray-900">All Bills</h1>

                <div className="flex flex-wrap gap-3 w-full md:w-auto items-center">
                    {/* Search */}
                    <div className="relative flex-1 md:w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search customer..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500"
                        />
                    </div>

                    {/* Filter Type */}
                    <div className="relative">
                        <select
                            value={filterType}
                            onChange={handleFilterTypeChange}
                            className="px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500 bg-white"
                        >
                            <option value="all">All Time</option>
                            <option value="weekly">Last 7 Days</option>
                            <option value="monthly">This Month</option>
                            <option value="custom">Custom Range</option>
                        </select>
                    </div>

                    {/* Custom Date Inputs */}
                    {filterType === 'custom' && (
                        <div className="flex items-center gap-2">
                            <input
                                type="date"
                                value={startDate}
                                onChange={(e) => setStartDate(e.target.value)}
                                className="px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500"
                            />
                            <span className="text-gray-500">-</span>
                            <input
                                type="date"
                                value={endDate}
                                onChange={(e) => setEndDate(e.target.value)}
                                className="px-3 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-500"
                            />
                        </div>
                    )}

                    <button
                        onClick={handleExport}
                        className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors shadow-sm"
                    >
                        <Download className="w-4 h-4" />
                        Export
                    </button>
                </div>
            </div>

            <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
                <table className="w-full text-left">
                    <thead className="bg-gray-50 text-gray-500 text-sm font-medium">
                        <tr>
                            <th className="px-6 py-4">Bill ID</th>
                            <th className="px-6 py-4">Date</th>
                            <th className="px-6 py-4">Customer</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4">Items</th>
                            <th className="px-6 py-4 text-right">Amount</th>
                            <th className="px-6 py-4 text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                        {filteredBills.map((bill) => (
                            <tr key={bill.id} className="hover:bg-gray-50 transition-colors">
                                <td className="px-6 py-4 font-medium text-gray-900">#{bill.id}</td>
                                <td className="px-6 py-4 text-gray-500">
                                    {new Date(bill.date).toLocaleDateString()}
                                </td>
                                <td className="px-6 py-4">
                                    <div className="font-medium text-gray-900">{bill.customer_name}</div>
                                    <div className="text-xs text-gray-500">{bill.customer_phone}</div>
                                </td>
                                <td className="px-6 py-4">
                                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${bill.status === 'Paid'
                                        ? 'bg-green-100 text-green-800'
                                        : 'bg-red-100 text-red-800'
                                        }`}>
                                        {bill.status === 'Paid' ? (
                                            <CheckCircle className="w-3.5 h-3.5" />
                                        ) : (
                                            <XCircle className="w-3.5 h-3.5" />
                                        )}
                                        {bill.status || 'Unpaid'}
                                    </span>
                                    {bill.payment_mode && (
                                        <div className="text-xs text-gray-500 mt-1 pl-1">
                                            via {bill.payment_mode}
                                        </div>
                                    )}
                                </td>
                                <td className="px-6 py-4 text-gray-500">
                                    {bill.items.length} items
                                </td>
                                <td className="px-6 py-4 text-right font-bold text-gray-900">
                                    ₹{bill.total_amount.toFixed(2)}
                                </td>
                                <td className="px-6 py-4 text-center">
                                    <div className="flex justify-center items-center gap-3">
                                        <button
                                            onClick={() => window.open(`/invoice/${bill.id}`, '_blank')}
                                            className="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
                                        >
                                            Invoice
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        {loading && (
                            <tr>
                                <td colSpan="7" className="px-6 py-8 text-center text-gray-500">
                                    Loading bills...
                                </td>
                            </tr>
                        )}
                        {!loading && filteredBills.length === 0 && (
                            <tr>
                                <td colSpan="7" className="px-6 py-8 text-center text-gray-500">
                                    No bills found.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>

        </div >
    );
};

export default ViewBills;
