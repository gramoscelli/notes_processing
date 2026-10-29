SELECT provincia, COUNT(*) AS numero_ventas FROM ventas
   GROUP BY provincia HAVING COUNT(*) > 5