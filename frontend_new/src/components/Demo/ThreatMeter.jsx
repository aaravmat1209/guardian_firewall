import React from 'react';
import './ThreatMeter.css';

const ThreatMeter = ({ riskLevel, patterns, confidence, isActive, explanations, conversationTrend }) => {
  // Debug logging
  console.log('🔍 ThreatMeter DEBUG - Received patterns:', patterns);
  console.log('🔍 ThreatMeter DEBUG - Received explanations:', explanations);
  console.log('🔍 ThreatMeter DEBUG - Received conversationTrend:', conversationTrend);
  console.log('🔍 ThreatMeter DEBUG - Patterns type:', typeof patterns);
  console.log('🔍 ThreatMeter DEBUG - Patterns length:', patterns ? patterns.length : 'undefined');

  const getTrendMessage = (trend) => {
    switch(trend) {
      case 'escalating':
        return 'Conversation risk is escalating';
      case 'de-escalating':
        return 'Conversation risk is de-escalating';
      case 'stable':
        return riskLevel > 30 ? 'Conversation risk is stable' : null;
      default:
        return null;
    }
  };

  const getTrendIcon = (trend) => {
    switch(trend) {
      case 'escalating':
        return '📈';
      case 'de-escalating':
        return '📉';
      case 'stable':
        return '📊';
      default:
        return '📊';
    }
  };

  const getThreatColor = (risk) => {
    if (risk <= 30) return '#10B981'; // Green
    if (risk <= 60) return '#F59E0B'; // Yellow
    return '#DC2626'; // Red
  };

  const getThreatLabel = (risk) => {
    if (risk <= 30) return 'LOW RISK';
    if (risk <= 60) return 'MEDIUM RISK';
    return 'HIGH RISK';
  };

  return (
    <div className={`threat-meter ${isActive ? 'threat-meter-active' : ''}`}>
      {/* Threat Level Bar */}
      <div className="threat-level">
        <div className="threat-level-header">
          <span className="threat-level-label">THREAT LEVEL</span>
          <span className="threat-level-value">{riskLevel}%</span>
        </div>
        <div className="threat-level-bar">
          <div 
            className="threat-level-fill"
            style={{
              width: `${riskLevel}%`,
              backgroundColor: getThreatColor(riskLevel),
              '--fill-color': getThreatColor(riskLevel)
            }}
          />
        </div>
        <div 
          className="threat-level-status"
          style={{ color: getThreatColor(riskLevel) }}
        >
          {getThreatLabel(riskLevel)}
        </div>
      </div>

      {/* Confidence Score */}
      <div className="threat-metric">
        <div className="threat-metric-label">CONFIDENCE SCORE</div>
        <div className="threat-metric-value">{confidence}%</div>
      </div>

      {/* Conversation Analysis */}
      <div className="threat-trend">
        <div className="threat-trend-label">CONVERSATION ANALYSIS</div>
        {getTrendMessage(conversationTrend) && (
          <div className="threat-trend-item">
            <span className="threat-trend-icon">🔍</span>
            <span className="threat-trend-text">{getTrendMessage(conversationTrend)}</span>
          </div>
        )}
        {riskLevel > 80 && (
          <div className="threat-trend-item">
            <span className="threat-trend-icon">🔍</span>
            <span className="threat-trend-text">User is suggesting a physical meeting, which is a serious threat.</span>
          </div>
        )}
      </div>

      {/* Patterns Detected */}
      <div className="threat-patterns">
        <div className="threat-patterns-label">PATTERNS DETECTED</div>
        <div className="threat-patterns-list">
          {patterns.length === 0 ? (
            <div className="threat-pattern-item threat-pattern-none">
              No threats detected
            </div>
          ) : (
            patterns.map((pattern, index) => (
              <div
                key={index}
                className={`threat-pattern-item ${pattern.severity}`}
                style={{ '--delay': `${index * 100}ms` }}
              >
                <span className="threat-pattern-icon">
                  {pattern.severity === 'high' ? '🚨' : pattern.severity === 'medium' ? '⚠️' : 'ℹ️'}
                </span>
                <span className="threat-pattern-text">{pattern.name}</span>
              </div>
            ))
          )}
        </div>
      </div>



      {/* Alert Banner for High Risk */}
      {riskLevel > 60 && (
        <div className="threat-alert">
          <div className="threat-alert-icon">⚠️</div>
          <div className="threat-alert-text">THREAT DETECTED</div>
        </div>
      )}
    </div>
  );
};

export default ThreatMeter;
