<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0"
    xmlns:tei="http://www.tei-c.org/ns/1.0">
    
    <xsl:output method="xml" indent="yes"/>
    
    <xsl:template match="/">
        <TEI>
            <teiHeader></teiHeader>
            <text>
                
            </text>
        
            <body>
                    <xsl:for-each select="//div[@n='3']">
                        <xsl:for-each select="./div">
                            <xsl:for-each select="./list">
                                <xsl:for-each select="./@subtype">
                                    <xsl:element name="p">
                                        <xsl:value-of select="."/>
                                    </xsl:element>
                                </xsl:for-each>
                            </xsl:for-each>
                        </xsl:for-each>
                    </xsl:for-each>
                
            </body>  
        </TEI>
    </xsl:template>
    

</xsl:stylesheet>