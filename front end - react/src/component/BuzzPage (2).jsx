import React, { useEffect, useState } from 'react';
import { Button } from 'primereact/button';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BellSoundPlayer = ({ frequencies, duration, onFinish }) => {
    const playBellSound = () => {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const gainNode = audioContext.createGain();
        gainNode.connect(audioContext.destination);

        frequencies.forEach(frequency => {
            const oscillator = audioContext.createOscillator();
            oscillator.type = 'sine'; // bell-like sound
            oscillator.frequency.setValueAtTime(frequency, audioContext.currentTime);
            oscillator.connect(gainNode);

            oscillator.start();
            oscillator.stop(audioContext.currentTime + duration);
        });

        gainNode.gain.setValueAtTime(1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + duration);

        // Call onFinish after the sound is played
        setTimeout(onFinish, duration * 1000);
    };

    useEffect(() => {
        playBellSound();
    }, []); // Play bell sound only on component mount

    return null;
};

const FirstComponent = () => {
    const [playBell, setPlayBell] = useState(false);
    const [alertTextVisible, setAlertTextVisible] = useState(true);
    const [selectedRecording, setSelectedRecording] = useState(null); // State to store the selected file
    const navigate = useNavigate();

    useEffect(() => {
        if (playBell) {
            const interval = setInterval(() => {
                setAlertTextVisible(prev => !prev);
            }, 500); // Toggle visibility every half second

            return () => clearInterval(interval);
        }
    }, [playBell]);

    useEffect(() => {
        const fetchAlert = async () => {
            try {
                const response = await axios.get('http://localhost:5000/alert');
                console.log(response.data.alert);
                
                if (response.data.alert) { // Check if the alert from the server is true
                    setPlayBell(true);
                } else {
                    setPlayBell(false);
                }
            } catch (error) {
                console.error('Error fetching alert:', error);
            }
        };

        const interval = setInterval(fetchAlert, 30000); // Check for alerts every 3 seconds

        return () => clearInterval(interval);
    }, []);

    const handleBellFinish = () => {
        setPlayBell(false);
        setAlertTextVisible(false);
    };

 
/**** */
    const handleRecordingChange = (event) => {
        setSelectedRecording(event.target.files[0]);
      };
    
      const handleUpload = async () => {
        if (!selectedRecording) {
          console.error('No recording selected');
          return;
        }
    
        const formData = new FormData();
        formData.append('recording', selectedRecording);
    
        try {
          const response = await fetch('http://localhost:5000/getRecording', {
            method: 'POST',
            body: formData
          });
    
          // Handle response from server if needed
        } catch (error) {
          console.error('Error:', error);
        }
      };


 /**** */     

    return (
        <div className="form-background">
            <div className="form-container" style={{ width: '25%', height: '98%' }}>
                <div className="p-card p-shadow-3 form-card" style={{ backgroundColor: '', height: '90%' }}>
                    <div className="p-card-header">
                        <h2>warn of a nearby mosquito</h2>
                    </div>
                    <div className="p-card-body">
                        <form>
                            <br />
                            {playBell && (
                                <div style={{ 
                                    visibility: alertTextVisible ? 'visible' : 'hidden',
                                    color: 'red', 
                                    fontSize: '1.2em', 
                                    fontWeight: 'bold', 
                                    textAlign: 'center', 
                                    border: '2px solid red', 
                                    padding: '10px', 
                                    borderRadius: '10px'
                                }}>
                                    Caution: Mosquitoes in the area! Stay vigilant!
                                </div>
                            )}
                            {playBell && <BellSoundPlayer frequencies={[440, 660, 880]} duration={2} onFinish={handleBellFinish} />}
                            <div style={{ marginTop: '300px' }}>
                                <input type="file" accept="audio/*" onChange={handleRecordingChange} />
                                <Button label="Send for inspection" onClick={handleUpload} style={{ marginTop: '100px' }} />
                            </div>
                            <Button label="Back to the menu" onClick={() => navigate('/thank-you')} style={{ marginTop: '20px' }} />
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FirstComponent;
