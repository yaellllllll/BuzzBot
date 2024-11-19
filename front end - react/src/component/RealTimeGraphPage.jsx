//לשאול את רות הזאת איך לעשות בגרך שמתי ששווה 5 זה ... וכו...



// export default RealTimeGraphPage;
import React, { useState, useEffect } from 'react';
import './RegistrationForm.css'; // ייבוא קובץ ה-CSS המותאם
import { Button } from 'primereact/button';
import { useNavigate } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import axios from 'axios';

// רישום הסקיילים והאלמנטים הדרושים
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const RealTimeGraphPage = () => {
    const [data, setData] = useState({ labels: [], datasets: [] });
    const [isDataLoaded, setIsDataLoaded] = useState(false);
    const navigate = useNavigate();
    const yLabels = ["very close",  "approaching", "far", "very far", "not around"];

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://localhost:5000/get-data');
                const newData = response.data;

                if (newData && Array.isArray(newData)) {
                    alert(newData)
                    const labels = newData.map((_, index) => (index + 1).toString());
                    // const modifiedData = newData.map(value => {
                    //     return value ==2  ? 'very far' : value; 
                    // });
                    const dataset = {
                        label: 'Real-Time Data',
                        data: newData,
                        borderColor: 'rgba(75,192,192,1)',
                        backgroundColor: 'rgba(75,192,192,0.2)',
                        fill: true,
                    };

                    setData({
                        labels: labels,
                        datasets: [dataset]
                    });
                    setIsDataLoaded(true);
                } else {
                    console.error('Received data is not in the expected format:', newData);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData(); // Fetch initial data
        const intervalId = setInterval(fetchData, 30000); // Fetch data every 3 seconds

        return () => clearInterval(intervalId); // Cleanup interval on component unmount
    }, []);

    const options = {
        scales: {
            y: {
                type: 'category',
                labels: yLabels
            }
        }
    };

    return (
        <div className="form-background">
            <div className="form-container" style={{ width: '25%', height: '98%' }}>
                <div className="p-card p-shadow-3 form-card" style={{ backgroundColor: '', height: '90%' }}>
                    <div className="p-card-header">
                        <h2>Real-Time Graph Page</h2>
                    </div>
                    <div className="p-card-body">
                        <form>
                            <br />
                            <div>
                                {isDataLoaded ? <Line data={data} options={options} /> : "Loading..."}
                            </div>
                            <Button label="Back to the menu" onClick={() => navigate('/thank-you')} style={{ marginTop: '90%' }} />
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RealTimeGraphPage;
