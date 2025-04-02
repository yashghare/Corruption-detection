export const exportToCSV = (data) => {
    const csvContent = [
      Object.keys(data).join(','),
      Object.values(data).join(',')
    ].join('\n');
  
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.style.display = 'none';
    link.href = url;
    link.download = `fraud_report_${new Date().toISOString().slice(0,10)}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  
  export const exportToPDF = async (elementId) => {
    const { jsPDF } = await import('jspdf');
    const { html2canvas } = await import('html2canvas');
    
    const element = document.getElementById(elementId);
    const canvas = await html2canvas(element, {
      scale: 2,
      logging: false,
      useCORS: true
    });
    
    const pdf = new jsPDF('p', 'mm', 'a4');
    const imgProps = pdf.getImageProperties(canvas);
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
    
    pdf.addImage(canvas, 'PNG', 0, 0, pdfWidth, pdfHeight);
    pdf.save(`fraud_report_${new Date().toISOString().slice(0,10)}.pdf`);
  };